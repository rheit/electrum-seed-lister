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
py ElectrumSeedLister.py abandon ability able about above absent absorb gronk absurd abuse access accident
```
Words that are not in the English word list will have words from the word list substituted for them. The following
output will be produced:
```
Not in word list: gronk
Standard wallet: abandon ability able about above absent absorb basic absurd abuse access accident
Standard wallet: abandon ability able about above absent absorb blanket absurd abuse access accident
Standard wallet: abandon ability able about above absent absorb color absurd abuse access accident
Standard wallet: abandon ability able about above absent absorb embark absurd abuse access accident
Standard wallet: abandon ability able about above absent absorb follow absurd abuse access accident
Standard wallet: abandon ability able about above absent absorb goddess absurd abuse access accident
Standard wallet: abandon ability able about above absent absorb hamster absurd abuse access accident
Standard wallet: abandon ability able about above absent absorb math absurd abuse access accident
Standard wallet: abandon ability able about above absent absorb obscure absurd abuse access accident
Standard wallet: abandon ability able about above absent absorb response absurd abuse access accident
Standard wallet: abandon ability able about above absent absorb sick absurd abuse access accident
Standard wallet: abandon ability able about above absent absorb system absurd abuse access accident
Standard wallet: abandon ability able about above absent absorb theme absurd abuse access accident
Standard wallet: abandon ability able about above absent absorb tip absurd abuse access accident
Standard wallet: abandon ability able about above absent absorb upset absurd abuse access accident
Standard wallet: abandon ability able about above absent absorb vocal absurd abuse access accident
```
You can then try creating a wallet with each of those seeds until you (hopefully) find your lost wallet.
There are only 16 possibilities in this particular case, which is pretty manageable compared to 2048 if
you were trying to substitute every word from the word list manually.