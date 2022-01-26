# CONTRIBUTING

Tut je pouky dlja programistov.

## Git-komity 

Projekt slěduje ugovoru [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0),
i zato, vaše komity potrěbujut imati podobnu strukturu:

```plain text
fix(hunspell): add new words
feat(chrome): add new banner image
chore(firefox): update dependencies
build(libreoffice): migrate scripts
docs(macos): update installer readme
refactor(npm): reduce coupling
ci(repo): update
```

kde v zatvorkah `(<package>)` to jest ime jednogo iz paketov v direktoriji `packages/`, abo
`repo`, ako komit někako vplivaje na cěly repozitorij.

Ako komit tyče se několikyh paketov, možete pisati jih črěz komu (`,`):

```
chore(firefox, chrome): update web manifest
```

## Zavisnosti projekta

* [Python 3.8 i vyše](https://www.python.org)
  * [lxml](https://lxml.de)
* [Node.js 14 i vyše](https://nodejs.org/en/)
  * [lerna](https://github.com/lerna/lerna)
* [Gnuplot](http://gnuplot.sourceforge.net)

## Projekty

Vse projekty sut v direktoriji `packages/` kako oddělne pakety,
ale, ako hčete instalovati jih jednočasno kako jedno čelo, možete
v korenju repozitorija izpustiti komandu:

```
npm install
```

> **POZORNOST**: trěba izpolniti prědhodne instrukcije iz
sekcije "Zavisnosti projekta" i imati vsu potrěbnu sbirku programov.

## TODO

Trěba bude ješče dopisati instrukcije.
