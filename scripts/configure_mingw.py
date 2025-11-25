import os
import shutil
import glob

# 1. Define the MinGW Path (Hardcoded based on your workflow setup)
MSYS_ROOT = r"C:\msys_build\msys64\mingw64"
MINGW_BIN = os.path.join(MSYS_ROOT, "bin")
#MINGW_LIB = os.path.join(MSYS_ROOT, "lib")
#MINGW_INC = os.path.join(MSYS_ROOT, "include")

def configure_distutils():
    """
    Creates a global pydistutils.cfg to establish mingw as compiler
    and to force MinGW compiler
    and inject necessary flags for Python 3.10/3.11 compatibility.
    """
    config_path = os.path.expanduser('~\\pydistutils.cfg')
    
    # define=MS_WIN64,SIZEOF_VOID_P=8 is crucial for Python 3.10/3.11 compatibility
    # on GCC to avoid "division by zero" errors in Cython.
    config_content = f"""[build]
compiler=mingw32

[build_ext]
compiler=mingw32
define=MS_WIN64,SIZEOF_VOID_P=8
"""
#include_dirs={MINGW_INC}
#library_dirs={MINGW_LIB}
    
    print(f"Writing global config to: {config_path}")
    with open(config_path, 'w') as f:
        f.write(config_content)

def alias_dlls():
    """
    Copies MinGW versioned DLLs (e.g., libiconv-2.dll) to the 
    standard names (e.g., iconv.dll) that the compiled wheel expects.
    """
    # Map: 'Pattern to find' -> 'Name to create'
    mappings = [
        ('libiconv-*.dll', 'iconv.dll'),
        ('libbz2-*.dll',   'libbz2.dll'),
        ('zlib1.dll',      'zlib.dll')
    ]

    print(f"Checking for DLLs in {MINGW_BIN}...")
    
    if not os.path.exists(MINGW_BIN):
        print(f"ERROR: MinGW bin directory not found at {MINGW_BIN}")
        return

    for pattern, alias in mappings:
        search_path = os.path.join(MINGW_BIN, pattern)
        matches = glob.glob(search_path)
        
        if not matches:
            print(f"WARNING: No file found matching {pattern}")
            continue
            
        src = matches[0] # Take the first match (e.g., libiconv-2.dll)
        dst = os.path.join(MINGW_BIN, alias)
        
        try:
            print(f"Copying {os.path.basename(src)} -> {alias}")
            shutil.copy2(src, dst)
        except Exception as e:
            print(f"Error copying {src}: {e}")

if __name__ == "__main__":
    configure_distutils()
    #alias_dlls()
    print("MinGW Configuration Complete.")
