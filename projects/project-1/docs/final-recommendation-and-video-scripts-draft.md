# Final recommendation and video scripts — draft

**Oladapo Olaniyan | FIN-43900 | October 15, 2026**  
**Status:** AI-assisted preparation. This is a draft presentation guide, not a recording, transcript, final student attestation, or submission.

## Recommended committee position for the current evidence

**Watch / defer initiation.** The base DCF value is **$117.29 per diluted-proxy share**, below the October 5, 2026 observed price of **$125.65** by about **6.7%**. The $76.12 low, $117.29 base, and $170.22 high outcomes are scenarios, not probability-weighted price targets. Terminal value is 80.1% of enterprise value, and the valuation still has qualified current-date bridge, comparable-company, working-capital, and terminal-ROIC assumptions.

The completed ROIC test reinforces the cautious position: changing terminal ROIC from 15.0% to 12.0% lowered base value per share from **$117.29 to $111.41**, a **$5.88 (5.02%)** decline. The prediction and separate run are recorded in `repro/locked-change-20261015T1722CDT/locked-test-report.md`.

**Proposed committee ask:** do not initiate at the recorded market price. Reconsider only after a reviewed valuation/current-date bridge and evidence of margin and cash recovery, or at a price that provides a defensible margin of safety. The working memo proposes an initial review point near a 20% discount to its base value, about **$93.84**, but Oladapo Olaniyan must accept, revise, or reject that threshold.

**Reversal trigger:** do not initiate if structural margin erosion, weaker cash conversion, or insufficient funding under the downside case becomes evident. Reconsider if later filings support a stronger margin/cash trajectory and an updated valuation supports the market price.

### If you keep your earlier BUY position

Say plainly that it differs from the current model rather than presenting it as model-supported. Before using BUY as the final committee action, add your own evidence-based answer to this sentence:

> I accept the risk that the current base DCF is below market price because [specific evidence from a dated filing or release], and I believe [specific model assumption] is conservative enough that an updated valuation would support entry.

Do not use “the company is doing well” by itself. Link the claim to a dated operating measure and explain why it changes value per share, not only revenue or EPS.

## Video 1 script — research evolution and AI check (target 2:30–2:50)

**Show:** `docs/research-evolution-v3.md`, the preserved Edition A recovery evidence, then `sources/` and `validation-and-ai-use-working.md`.

> I am Oladapo Olaniyan, and this is my Project 1 research-evolution review of PepsiCo. My working decision is watch and defer rather than an immediate purchase. The original Edition A evidence is preserved separately because the available PDF contains an error page; I did not recreate it or claim unavailable content.
>
> In Edition B, I rebuilt the valuation around PepsiCo's FY2025 filings and the latest interim bridge used in the model. An important correction was capital spending. I distinguish the consolidated cash-flow capex of $4,415 million from the segment amount of $4,192 million plus $223 million of corporate capex. That correction avoids treating a partial segment number as the consolidated total.
>
> AI helped with source organization, model code, and draft documentation. I checked material values against primary-source arithmetic and ran the model's validation checks. My recorded AI use and limitations are in the validation record. The terminal-ROIC changed-input test was AI-assisted after the in-class clarification reported on October 15. Lowering terminal ROIC from 15 percent to 12 percent lowered value per share from $117.29 to $111.41, which matched the pre-run prediction.
>
> The main unresolved issues are the current-date bridge, some peer comparability inputs, working-capital reconciliation, and final student judgment. Those are why this is a watch/defer recommendation rather than a final price target.

## Video 2 script — model, finance mechanics, and validation (target 4:15–4:45)

**Show:** `src/model.py`, `data/assumptions.json`, `outputs/final-working-run/visible-output.html`, `outputs/final-working-run/checks.csv`, and `repro/cold-20261006T053603935700Z/cold-run-evidence.json`.

> This video walks through the PepsiCo FCFF valuation and its checks. The workflow moves from filing inputs, to assumptions, to linked forecast statements, FCFF, the DCF, the enterprise-to-equity bridge, and this visible output.
>
> The forecast runs from fiscal 2026 through 2030. FY2026 growth is anchored to management's four to six percent outlook, while later growth, margins, capex, tax, beta, equity-risk premium, debt spread, terminal growth, and terminal ROIC are assumptions that remain open for final judgment.
>
> FCFF begins with operating profit after tax. I incorporate noncash items and working-capital investment, and I keep financing effects out of FCFF. The terminal value funds growth through reinvestment: terminal NOPAT times growth divided by incremental ROIC. With a 2.5 percent terminal growth rate and 15 percent ROIC, the terminal reinvestment rate is 16.67 percent.
>
> In the base case, WACC is 7.66 percent, terminal growth is 2.5 percent, and value per diluted-proxy share is $117.29. The recorded market price is $125.65. Terminal value represents 80.1 percent of enterprise value, so small long-run assumptions matter.
>
> The ordinary validation run contains 42 passes, zero failures, five open items, and two qualified items. It includes statement articulation, bridge calculations, WACC and terminal-growth direction checks, synthetic known answers, and a deliberate cash-ledger corruption test. A clean environment rerun reproduced the principal output files. These checks show that the documented calculations run; they do not prove every economic assumption.
>
> I also completed a separate changed-input test. Reducing terminal ROIC from 15 percent to 12 percent increased terminal reinvestment, lowered terminal FCFF, and reduced value per share to $111.41. That matched the recorded prediction. The full inputs, outputs, and limitations are in the locked-test report.

## Video 3 script — live product demonstration and committee ask (target 4:00–4:35)

**Show live:** `outputs/final-working-run/visible-output.html`; scroll through the scenario table, sensitivity grid, reverse DCF, and peer section. Keep this screen as the main part of the video.

> My current committee recommendation is watch and defer initiation in PepsiCo. The recorded October 5 price is $125.65, while the base DCF value is $117.29 per share. The scenario values are $76.12 in the low case, $117.29 in the base case, and $170.22 in the high case. I use those as conditional outcomes, not probability-weighted targets.
>
> Here is the live output. The model shows the principal inputs, five-year forecast, FCFF, and valuation bridge. The base WACC is 7.66 percent, terminal growth is 2.5 percent, and terminal value is 80.1 percent of enterprise value. That concentration means I should be cautious about treating a single DCF point estimate as enough to buy.
>
> This table shows the Value Reset Failure case. It connects weaker revenue, lower gross margin, higher SG&A, and longer receivable and inventory days to lower FCFF, cash funding needs, debt, and value. It is a modeled risk scenario, not a claim that PepsiCo will default.
>
> The sensitivity grid tests WACC and terminal growth. The reverse DCF shows one conditional path to the market price: roughly 0.85 percentage points more EBIT margin across forecast years, holding other inputs fixed. The peer lenses are qualified and I do not average them with the DCF because the accounting and comparability gaps are unresolved.
>
> My ask is to defer entry while monitoring organic volume and pricing, North American margin, inventory and receivable days, cash conversion, debt, and payouts after each release. I would reconsider after a reviewed current-date bridge and verified margin and cash recovery, or at a defensible margin of safety. If structural margin erosion or insufficient downside funding appears, I would not initiate.

## Recording checklist

1. Record each video once using the script as notes, then make only factual corrections while reviewing it.
2. Record the measured duration, title, stable URL, and exact topic timestamps in the manifest.
3. Create each transcript from the actual recording; correct financial terms, amounts, ticker names, and any words that change meaning.
4. Check the repository and every video link while logged out before freezing the package.
5. Update the memo, visible output, validation record, transcripts, and manifest together if you change the committee action.
