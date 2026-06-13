# il0v3pdfs

**Idea:** The visible page only shows a decoy string. The real flag sits in the **page content stream** as a **PDF comment** (`%` … end of line). Renderers skip those bytes, so copy/paste and normal “text layer” views look useless.

**Solve:** `strings il0v3pdfs.pdf | grep CPCTF`, hex-edit the file, or search for `% CPCTF` in the content stream after the dummy `TJ` text.

**Flag:** `CPCTF{Lets_P1ey_W1th_PdFs}`
