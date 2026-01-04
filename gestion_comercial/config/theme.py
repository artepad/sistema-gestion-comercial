class Theme:
    """
    Centralized visual style configuration based on 'Contador de Caja'.
    """
    
    # Main Window Colors
    BACKGROUND = '#f8f9fa'  # Light gray background
    TEXT_PRIMARY = '#2c3e50' # Dark blue-gray for main text
    
    # Section Colors
    # Bills Section (Greenish)
    BILLS_BG = '#e8f5e8'
    BILLS_FG = '#27ae60'
    
    # Coins Section (Yellowish)
    COINS_BG = '#fff3cd'
    COINS_FG = '#856404'
    
    # Total Section (Blueish)
    TOTAL_BG = '#e3f2fd'
    TOTAL_FG = '#1565c0'
    TOTAL_TEXT = '#0d47a1'
    
    # UI Elements
    ENTRY_BG = 'white'
    BUTTON_CLEAN_BG = '#6c757d' # Gray
    BUTTON_CLEAN_FG = 'white'
    BUTTON_EXIT_BG = '#dc3545'  # Red
    BUTTON_EXIT_FG = 'white'
    
    # Fonts
    # Using Segoe UI as a modern alternative to Arial for Windows, 
    # but keeping the sizes and weights consistent with the request.
    FONT_FAMILY = 'Segoe UI' 
    
    FONTS = {
        'h1': (FONT_FAMILY, 20, 'bold'),
        'h2': (FONT_FAMILY, 16, 'bold'),
        'h3': (FONT_FAMILY, 14, 'bold'),
        'body': (FONT_FAMILY, 11),
        'body_bold': (FONT_FAMILY, 11, 'bold'),
        'total_large': (FONT_FAMILY, 24, 'bold'),
        'button': (FONT_FAMILY, 12, 'bold'),
        'icon_large': (FONT_FAMILY, 48),
    }
