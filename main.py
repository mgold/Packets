from virus.main import main
try:
    import android
except ImportError:
    android = None

# Map the back button to the escape key.
if android:
    android.init()
    android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

main()
