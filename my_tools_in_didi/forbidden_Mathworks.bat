@echo off

setlocal EnableDelayedExpansion
color 3e
title Set MATLAB Environment
 
PUSHD %~DP0 & cd /d "%~dp0"
%1 %2
mshta vbscript:createobject("shell.application").shellexecute("%~s0","goto :runas","","runas",1)(window.close)&goto :eof
:runas
 
::MATLAB
set "hosts_file=C:\Windows\System32\drivers\etc\hosts"

echo # >> %hosts_file%
echo # ------ MATLAB start ------ >> %hosts_file%
echo # >> %hosts_file%
echo 127.0.0.1  www.mathworks.com authnz.mathworks.com >> %hosts_file%
echo ::1        www.mathworks.com authnz.mathworks.com >> %hosts_file%
echo 127.0.0.1  login.mathworks.com assets.adobedtm.com dpm.demdex.net smetrics.mathworks.com dws.mathworks.com >> %hosts_file%
echo ::1        login.mathworks.com assets.adobedtm.com dpm.demdex.net smetrics.mathworks.com dws.mathworks.com >> %hosts_file%
echo # >> %hosts_file%
echo # ------  MATLAB end  ------ >> %hosts_file%
 
echo 执行完毕,任意键退出
 
pause >nul
exit

