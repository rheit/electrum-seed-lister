# Electrum Seed Lister

If you already have a mostly correct Electrum wallet seed but find that one of the words is wrong,
you can use this script to list all the potentially valid seeds. Then you can try recreating the wallet with
the seeds listed until you (hopefully) find the correct one.

If you're desperate, it will also work with more than one invalid word, although the list will be
much larger than if you had only one bad word.

### Prerequesites

You need Python. Tested with Python 3.6.

### Usage

Pass your best seed guess to the command line. e.g.

```
py ElectrumSeedLister.py abandon ability able about above absent absorb abstract absurd abuse access accident
```
Words that are not in the English word list will have words from the word list substituted for them.
