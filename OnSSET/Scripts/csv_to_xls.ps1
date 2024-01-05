# CSV Bulk Converter Script
# This PowerShell script converts all CSV files in a specific location to XLSX format. 
# It uses the Microsoft Excel COM object to open each CSV file, convert it to a table, and save it as an XLSX file.
# The converted files are saved in the same location as the original CSV files.
# NOTE: This script will convert all CSV files in the specified location, so use with caution.
 
# - Specify the delimiter used in the CSV file.
$csvDelimiter = ","  
 
# - Path to CSV files. (WARNING: ALL CSV FILES WILL BE CONVERTED )
#$csvLocation = "C:\temp\CSV Converter"
$csvLocation = "C:\FEEM\GEP\Kenya\scenarios"
# - Code
foreach ($csvFile in Get-Childitem -Path $csvLocation  -Filter "*.csv") {
Write-Host -ForegroundColor Green "Converting file '$($csvFile.BaseName)' to XLSX format."
$excel = New-Object -ComObject excel.application
$xlsxFilepath = "$csvLocation\$($csvFile.BaseName).xlsx"
    $workbook = $excel.Workbooks.Add(1)
    $worksheet = $workbook.worksheets.Item(1)
$csvFilepath = ("TEXT;" + $csvFile.FullName)
    $csvConnector = $worksheet.QueryTables.add($csvFilepath, $worksheet.Range("A1"))
        $query = $worksheet.QueryTables.item($csvConnector.name)
        $query.TextFileOtherDelimiter = $csvDelimiter
        $query.TextFileParseType  = 1
        $query.TextFileColumnDataTypes = ,1 * $worksheet.Cells.Columns.Count
        $query.AdjustColumnWidth = 1
        $query.TextFilePlatform = 65001 # UTF8 fix
        $query.Refresh()| Out-Null
        $query.Delete()
Add-Type -AssemblyName "Microsoft.Office.Interop.Excel"
    $worksheet.Columns.AutoFit() | Out-Null
        $table = $excel.ActiveSheet.ListObjects.Add([Microsoft.Office.Interop.Excel.XlListObjectSourceType]::xlSrcRange, $excel.ActiveCell.CurrentRegion, $null ,[Microsoft.Office.Interop.Excel.XlYesNoGuess]::xlYes)
        $table.Name = "TableData"
        $table.TableStyle = "TableStyleMedium20"
    $workbook.SaveAs($xlsxFilepath,51)
    $excel.Quit()
# - Comment out the section below if you don't want to remove the CSV file after converting.
if (Test-Path "$csvLocation\$($csvFile.BaseName).xlsx") {
    Remove-Item -Path $($csvFile).FullName -Force}
}