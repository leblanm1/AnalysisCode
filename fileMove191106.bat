@echo off
pushd C:\Users\lebla\Desktop\fca\July_Boulder_Data\191106
for /f "tokens=* delims=" %%a in ('type GoodFilesSptP_191106.txt') do xcopy /hrkvy ".\3\%%a" ".\Destination"
popd
pause