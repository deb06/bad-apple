@if (@a==@a) @then

@echo off

set SendKeys=CScript //nologo //E:JScript "%~F0"
%SendKeys% {F11};

python main.py
pause >nul

@end
var WshShell = WScript.CreateObject("WScript.Shell");
WshShell.SendKeys(WScript.Arguments(0));