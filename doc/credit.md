I tried scraping credit data, but this has proven somewhat difficult due to the
variety of formatting used. The first attempt, which works for most but not
nearly all cases, is provided here for reference.

    credit_enc = re.search('<b>.*?(Credit|Courtesy).*?</b>\s*(.*?)\s*(</center>)?\s*<p>', apod_html, regex_flags).group(2)
    credit_dec = credit_enc.decode('latin-1')
    credit = oneline(credit_dec)
