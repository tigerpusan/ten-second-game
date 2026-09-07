from pathlib import Path

html = Path('www/index.html').read_text()
icons = Path('scripts/generate_icons.py').read_text()

assert '10초 맞추기' in html
assert 'MASTER_VOLUME' in html and '0.10' in html
assert 'playResultSound' in html and 'playTick' in html
assert 'remove_adaptive_icons' in icons
assert 'mipmap-anydpi-v26' in icons
assert 'ic_launcher.xml' in icons and 'ic_launcher_round.xml' in icons

print('verification passed')