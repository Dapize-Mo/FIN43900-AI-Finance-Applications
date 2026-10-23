# Oladapo Olaniyan - FIN-43900 independent local recording check.
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$taskOut = Join-Path $PSScriptRoot 'audio-check'
foreach ($taskNumber in 1..3) {
    $taskEngine = [System.Speech.Recognition.SpeechRecognitionEngine]::new([cultureinfo]'en-US')
    $taskGrammar = [System.Speech.Recognition.DictationGrammar]::new()
    $taskEngine.LoadGrammar($taskGrammar)
    $taskEngine.SetInputToWaveFile((Join-Path $taskOut "video-$taskNumber.wav"))
    $taskSegments = [System.Collections.Generic.List[object]]::new()
    Write-Output "START VIDEO $taskNumber"
    while ($null -ne ($taskResult = $taskEngine.Recognize())) {
        $taskEntry = [pscustomobject]@{
            start = $taskResult.Audio.AudioPosition.TotalSeconds
            duration = $taskResult.Audio.Duration.TotalSeconds
            text = $taskResult.Text
            confidence = $taskResult.Confidence
        }
        $taskSegments.Add($taskEntry)
        Write-Output "$taskNumber [$($taskEntry.start)] $($taskEntry.text)"
    }
    $taskSegments.ToArray() | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $taskOut "video-$taskNumber-windows-asr.json") -Encoding utf8
    $taskEngine.Dispose()
    Write-Output "COMPLETE VIDEO $taskNumber"
}
