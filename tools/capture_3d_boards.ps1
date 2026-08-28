# Captures the real 3D board of every checkers variant for the website.
#
# The 3D board is three.js inside a WebView (lib/board3d/dama3d_scene.dart), so
# it cannot be rendered by any Dart-side tool. This renders the exact page the
# apps ship - assets/dama3d_web/dama3d.html - in headless Chrome and screenshots
# it, the same technique used for Chess Ta! (chess_master/tool/capture_board3d.ps1).
#
# The store_assets folders do NOT contain 3D screenshots. Their xr_* images are
# wide-screen 2D layouts, and turkish-cli's store_assets are byte-identical
# copies of dama-cli's. So these captures are the only real 3D art available.
#
# Run from the repo root:
#   powershell -ExecutionPolicy Bypass -File tools/capture_3d_boards.ps1
#
# Requires Chrome and python on PATH. SwiftShader is mandatory: headless Chrome
# with no GPU renders a blank WebGL canvas without it.

$ErrorActionPreference = 'Stop'

$gameRoot = 'D:\PortableGit\home\02 gameproject'
$outRoot  = Join-Path $PSScriptRoot '..\assets\img'

$chrome = @(
  "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
  "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
  "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
) | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $chrome) { throw 'Chrome not found.' }

# repo -> slug, board size, layout.
#   'diag'   = pieces on dark squares only, N rows a side (8x8 and 10x10 draughts)
#   'ortho'  = Turkish: every square playable, rows 1-2 and 5-6 fully filled
$variants = @(
  @{ repo = 'dama-cli';               slug = 'dama-ta';       n = 8;  rows = 3; layout = 'diag'  },
  @{ repo = 'brazilian-cli';          slug = 'brazilian';     n = 8;  rows = 3; layout = 'diag'  },
  @{ repo = 'english-dama-cli';       slug = 'english';       n = 8;  rows = 3; layout = 'diag'  },
  @{ repo = 'rusian-dama-cli';        slug = 'russian';       n = 8;  rows = 3; layout = 'diag'  },
  @{ repo = 'international-dama-cli'; slug = 'international'; n = 10; rows = 4; layout = 'diag'  },
  @{ repo = 'turkish-cli';            slug = 'turkish';       n = 8;  rows = 2; layout = 'ortho' }
)

$harnessTemplate = @'
<title>3d capture harness</title>
<style>html,body{margin:0;padding:0;overflow:hidden;background:#000}
iframe{border:0;display:block;width:100vw;height:100vh}</style>
<!-- Board size is read from the URL (?n=), not the sync payload - see BOARD_N in
     dama3d.html. Omitting it silently builds an 8x8 board, and a 10x10 layout
     then spills its pieces onto the table. -->
<iframe id="f" src="dama3d.html?n=__N__"></iframe>
<script>
  // Codes come from dama3d.html: p/P = player man/king, a/A = AI man/king.
  const N = __N__, ROWS = __ROWS__, LAYOUT = "__LAYOUT__";
  const pieces = [];
  for (let r = 0; r < N; r++) {
    for (let c = 0; c < N; c++) {
      const playable = LAYOUT === 'ortho' ? true : ((r + c) % 2 === 1);
      if (!playable) continue;
      if (LAYOUT === 'ortho') {
        // Turkish: men start on ranks 2-3 and 6-7, back rank stays empty.
        if (r === 1 || r === 2) pieces.push({ code: 'a', row: r, col: c });
        else if (r === N - 2 || r === N - 3) pieces.push({ code: 'p', row: r, col: c });
      } else {
        if (r < ROWS) pieces.push({ code: 'a', row: r, col: c });
        else if (r >= N - ROWS) pieces.push({ code: 'p', row: r, col: c });
      }
    }
  }
  const state = { playerIsBlack: false, pieces: pieces };
  const f = document.getElementById('f');
  f.addEventListener('load', () => {
    const push = () => {
      const w = f.contentWindow;
      if (!w || typeof w.syncBoard !== 'function') return setTimeout(push, 100);
      w.syncBoard(state);
      setTimeout(() => w.syncBoard(state), 1500); // meshes load lazily
    };
    push();
  });
</script>
'@

$port = 8791
foreach ($v in $variants) {
  $web = Join-Path $gameRoot "$($v.repo)\dama_master\assets\dama3d_web"
  if (-not (Test-Path $web)) { Write-Host "SKIP $($v.repo): no dama3d_web"; continue }

  $out = Join-Path $outRoot $v.slug
  New-Item -ItemType Directory -Force $out | Out-Null

  $harness = Join-Path $web '_cap3d.html'
  $server = $null
  try {
    $html = $harnessTemplate.Replace('__N__', $v.n).Replace('__ROWS__', $v.rows).Replace('__LAYOUT__', $v.layout)
    Set-Content -Path $harness -Value $html -Encoding utf8
    $server = Start-Process -PassThru -WindowStyle Hidden -WorkingDirectory $web `
      -FilePath 'python' -ArgumentList '-m', 'http.server', "$port", '--bind', '127.0.0.1'
    Start-Sleep -Seconds 2

    foreach ($shot in @(@{ n = 'board3d'; w = 1400; h = 1000 }, @{ n = 'board3d_wide'; w = 1920; h = 1080 })) {
      $file = Join-Path $out "$($shot.n).png"
      # Chrome reports "N bytes written to file" on STDERR even on success. In
      # PowerShell 5.1 that surfaces as a NativeCommandError and, under
      # ErrorActionPreference=Stop, aborts the whole run - so drop to Continue
      # around the call and judge success by whether the file appeared.
      $prev = $ErrorActionPreference
      $ErrorActionPreference = 'Continue'
      & $chrome --headless=new --disable-gpu --use-angle=swiftshader `
        --enable-unsafe-swiftshader --hide-scrollbars --force-device-scale-factor=1 `
        --window-size="$($shot.w),$($shot.h)" --virtual-time-budget=45000 `
        --screenshot="$file" "http://127.0.0.1:$port/_cap3d.html" | Out-Null
      $ErrorActionPreference = $prev
      if (Test-Path $file) {
        Write-Host ("  {0,-16} {1,-14} {2} bytes" -f $v.slug, $shot.n, (Get-Item $file).Length)
      } else {
        Write-Host "  $($v.slug) $($shot.n) FAILED"
      }
    }
  }
  finally {
    if ($server -and -not $server.HasExited) { Stop-Process -Id $server.Id -Force }
    if (Test-Path $harness) { Remove-Item $harness -Force }
  }
}
Write-Host "`nDone. 3D captures written under assets/img/<slug>/."
