# Recording and transcript check

Oladapo Olaniyan | FIN-43900 Project 1 | October 17, 2026

## Result

Keep the three recordings. The independent automated audio comparison did not identify a major numerical error or missing principal topic requiring a rerecording. This is an audio/content comparison and sampled frame review, not a predicted grade or a claim of human word-for-word listening.

| Video | Measured duration | Course maximum | Result |
|---|---:|---:|---|
| 1 - Research evolution / AI | 2:16.405 | 3:00 | Within limit; keep, with outdated-screen clarification |
| 2 - Model / validation | 4:08.768 | 5:00 | Within limit; keep; update topic timestamps |
| 3 - Committee presentation | 4:41.240 | 5:00 | Within limit; keep; distinguish spoken explanations from visual demonstrations |

All three matching M4A files were decoded and processed in full using faster-whisper small.en, CPU/int8, beam size 1. The audio stayed local. Audio/video duration pairs agree to within 0.003 seconds. Paths, durations, and SHA256 hashes are in recording-metadata.json. Original downloaded transcripts and recordings were preserved.

## Financial checks against the saved executed project

- Capex: $4.192 billion segments + $0.223 billion corporate = $4.415 billion consolidated. The recorded capex explanation is supported by the independent recognition and project reconciliation.
- Low/base/high values: $76.12 / $117.29 / $170.22; recorded reference market price $125.65. Video 2 and Video 3 recognition supports these figures.
- Base WACC: 7.6614988167%, correctly stated as approximately 7.66%; terminal growth 2.5%; terminal share 80.1178894510%, correctly rounded to 80.1%.
- Validation counts: 42 PASS, 0 FAIL, 5 OPEN, 2 QUALIFIED, matching checks.csv. Open/qualified checks must remain disclosed.
- ROIC test: 15% -> 12%; baseline 117.2940729555 -> 111.4096394030. Decline $5.8844335525, or 5.0168208881%, correctly rounded to $5.88 and 5.02%. The web review's suggestion that 5.02% was an error was based on already-rounded display values.
- Reverse DCF: uniform EBIT-margin shift 0.0084687699, equal to 0.84687699 percentage points, correctly rounded to approximately 0.85 percentage points. It is conditional on the other inputs, not a unique market forecast.
- Video 3 recognition includes the downside case, sensitivity, reverse DCF, qualified Coca-Cola/Mondelez comparisons, rejection of mechanical averaging, and final watch/defer conditions.
- Cold-run evidence reports exit 0 and five matching principal output hashes. Old labs/project-1 paths in that historical log reflect the former project location; they should not be represented as the current run command.

These checks establish consistency with existing project evidence. They do not refresh or independently reverify the historical market/filing sources.

## Transcript changes and limitations

The three new transcript-video-N-audio-compared.txt files retain the supplied draft wording and separate editorial notes. Topic timestamps were aligned to phrases in the independently recognized audio. Segment interpolation means they are approximate navigation markers, not frame-exact or word-level caption timings. topic-timestamp-comparison.csv records each change.

Material timing changes include Video 2 assumptions at about 0:59, results at 1:31, terminal-value explanation at 2:04, validation at 2:26, clean run at 3:12, and closing at 3:45. Video 3 committee ask starts about 4:04, rather than the supplied 3:56.

The independent recognizer makes obvious errors in the student's name, PepsiCo, and some financial terms. It must not replace the whole transcript blindly. Retain these narrowly scoped uncertainties for final playback review:

1. Video 1, approximately 1:34-1:59: ROIC expansion, "reinstated and reinvested," and "performance ability/performability." The monetary-result phrase is also imperfectly recognized locally; the supplied draft and model agree on $111.41. Do not silently replace a spoken slip with the technically correct phrase.
2. Video 2, approximately 1:14-1:19: "return on investment cost" is a spoken ROIC expansion error supported by both sources. Standard expansion: return on invested capital. Keep spoken wording and the separate correction. Approximately 2:41-2:48, the exact "checks ... I meant items" self-correction remains imperfectly recognized; the four validation totals are supported.
3. Video 3, approximately 1:15: "base cap case"; approximately 1:51-2:00: a reinvestment sentence stumble. The supplied draft smooths part of the latter passage; local recognition suggests "it is required if it requires." These do not change the investment conclusion, but exact filler is not certified.

Thus the files are audio-compared drafts with corrected topic timing. They should not be mislabeled as independently human-certified verbatim transcripts. No finance correction was silently inserted into the spoken text.

## Sampled video evidence

Frames were decoded at exact requested timestamps (not merely the preceding keyframe):

- Video 1 at 0:35, 1:15, 1:48: webcam and research/validation pages visible. The old screen still says staff guidance unresolved and shows working validation rows. Reconcile this with docs/staff-guidance-user-reported-v3-20261017.md and the actual completed checks in the written package. The recording itself remains unchanged.
- Video 2 at 0:18, 2:35, 3:20: model code, checks CSV, and cold-run JSON visibly displayed. Main evidence is usable; dense source text requires full-resolution playback. The sampled frame still shows editor problem badges; the frame alone does not establish a runtime failure. Historical cold-run output is the executable evidence.
- Video 3 at 2:30, 3:10, 3:45: the browser displays scenario and forecast summary tables with webcam visible. Do not claim these timestamps visually demonstrate the expanded sensitivity grid or peer details. They support the live output summary; reverse DCF and peers are spoken explanations, with detailed evidence supplied in repository outputs.

This was a nine-frame sample, not continuous video playback. The existing recordings need not be redone solely for pauses, duplicate webcam views, or small wording slips. The final manifest must accurately index what is spoken versus actually shown.

## Files and reproducibility

Final check artifacts in this folder: this report; three audio-compared transcript drafts; topic-timestamp-comparison.csv; recording-metadata.json.

Intermediate local evidence and setup remain under ../../tmp/: audio-check/video-1-asr.json through video-3-asr.json; three exact-frame review sheets; WAV decoding copies; local model files and isolated audio-check-env; check_recording_audio.py, decode_audio_check.py, native_audio_check.ps1, recording_screen_check.py, and build_audio_check_report.py. These are check tooling, not submission dependencies. A Windows-recognizer fallback was inaccurate and not used as the transcript source. The successful local faster-whisper pass is the comparison basis.

Remaining packaging work: reconcile dated working screens in the written documents, complete the final transcript review of the narrow uncertain passages, add hosted repository/video URLs and access checks, and assemble mutually consistent final deliverables. Nothing was submitted or published during this check.
