## Install required Python packages
$Packages = Get-Content requirements.txt
foreach ($Package in $Packages) {
    Write-Host "Installing $package"
    pip install $Package
}
