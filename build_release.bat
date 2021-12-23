set "exePath_upx=C:\upx-3.96-win64\upx.exe"
set "exePath_7zip=.\7zip\7za.exe"

@echo off
cls

goto nuitkac

:nuitkac
python -m nuitka --standalone .\r6launcher.py --include-data-file=./assets/*.*=assets/ --enable-plugin=pyqt5 --python-flag=-OO --windows-disable-console
goto delete_useless_files

:delete_useless_files
del r6launcher.dist\assets\splash_screen.png
del r6launcher.dist\libcrypto-1_1.dll
del r6launcher.dist\qt5quick.dll
del r6launcher.dist\libeay32.dll
del r6launcher.dist\tcl86t.dll
del r6launcher.dist\sqlite3.dll
del r6launcher.dist\tk86t.dll
del r6launcher.dist\qt5network.dll
del r6launcher.dist\unicodedata.pyd
del r6launcher.dist\ucrtbase.dll
del r6launcher.dist\qt5multimedia.dll
del r6launcher.dist\_tkinter.pyd
del r6launcher.dist\qt5printsupport.dll
del r6launcher.dist\qt5svg.dll
del r6launcher.dist\qt5qmlmodels.dll
del r6launcher.dist\qt5dbus.dll
del r6launcher.dist\libssl-1_1.dll
del r6launcher.dist\ssleay32.dll
del r6launcher.dist\lib2to3 /Q
rd r6launcher.dist\lib2to3
goto upx_compress

:upx_compress
%exePath_upx% .\r6launcher.dist\r6launcher.exe .\r6launcher.dist\qt5gui.dll .\r6launcher.dist\qt5core.dll .\r6launcher.dist\qt5widgets.dll .\r6launcher.dist\python39.dll .\r6launcher.dist\qt5qml.dll --lzma -1
goto 7zip_compress

:7zip_compress
%exePath_7zip% a -t7z -mx=9 -mfb=273 -ms -md=31 -myx=9 -mtm=- -mmt -mmtf -md=1536m -mmf=bt3 -mmc=10000 -mpb=0 -mlc=0 R6Launcher.7z ./r6launcher.dist/*
goto done

:done
pause