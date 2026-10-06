# reading-helper

Personal reading-study helpers, published with GitHub Pages.

## HPMOR summaries — [`hpmor/`](hpmor/)

Parallel 4-column study tables for *Harry Potter and the Methods of
Rationality* by Eliezer Yudkowsky:

1. Verbatim English content (byte-for-byte, mechanically verified)
2. Summarized English content
3. Persian translation, as close to verbatim as possible
4. Persian summarization

Chapters so far: **7. Reciprocation**, **8. Positive Bias**, **9. Title Redacted, Part I**, **10. Self Awareness, Part II**, **11. Omake Files 1, 2, 3**, **12. Impulse Control**, **13. Asking the Wrong Questions**, **14. The Unknown and the Unknowable**, **15. Conscientiousness**, **16. Lateral Thinking**, **17. Locating the Hypothesis**, **18. Dominance Hierarchies**, **19. Delayed Gratification**, **20. Bayes's Theorem**, **21. Rationalization**, **22. The Scientific Method**, **23. Belief in Belief**, **24. Machiavellian Intelligence Hypothesis**, **25. Hold Off on Proposing Solutions**.

Verify locally: `cd hpmor && python3 scripts/verify.py`
Rebuild pages: `cd hpmor && python3 scripts/build_chapter7.py && python3 scripts/build_chapter8.py && python3 scripts/build_chapter9.py && python3 scripts/build_chapter10.py && python3 scripts/build_chapter11.py && python3 scripts/build_chapter12.py && python3 scripts/build_chapter13.py && python3 scripts/build_chapter14.py && python3 scripts/build_chapter15.py && python3 scripts/build_chapter16.py && python3 scripts/build_chapter17.py && python3 scripts/build_chapter18.py && python3 scripts/build_chapter19.py && python3 scripts/build_chapter20.py && python3 scripts/build_chapter21.py && python3 scripts/build_chapter22.py && python3 scripts/build_chapter23.py && python3 scripts/build_chapter24.py && python3 scripts/build_chapter25.py`

Live site: <https://hkalbasi.github.io/reading-helper/hpmor/>
