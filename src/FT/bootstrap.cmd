@echo off
powershell Set-ExecutionPolicy RemoteSigned
powershell %cd%\tools\simplplus\mass-usp-compiler\mass-usp-compiler.ps1 -Path . -series3
powershell Set-ExecutionPolicy Restricted
EXIT
