#!/bin/bash
# -*- coding: utf-8 -*-

# $1 is input (base).  It expects $1.dict to exist.
# $2 is the translation file

#
# Dieses Skript generiert deutsche Trennmuster.
#
# Aufruf:
#
#   sh make-full-pattern.sh words.hyphenated german.tr
#
#
# Eingabe: $1 Liste von getrennten Wörtern.
#          $2 Translationsdatei für patgen.
#
# Ausgabe: pattmp.[1-8]       patgen-Resultate.
#          $1.[0-8]      Trennmuster -- pattern.8 ist die finale
#                             Trennmusterdatei.
#          $1.[1-8].log  Log-Dateien.
#          $1.rules      Die patgen-Parameter in kompakter Form.
#


# Die Parameter für patgen für die Level eins bis acht.

hyph_start_finish[1]='1 1'
hyph_start_finish[2]='2 2'
hyph_start_finish[3]='3 3'
hyph_start_finish[4]='4 4'
hyph_start_finish[5]='5 5'
hyph_start_finish[6]='6 6'
hyph_start_finish[7]='7 7'
hyph_start_finish[8]='8 8'

pat_start_finish[1]='2 5'
pat_start_finish[2]='2 5'
pat_start_finish[3]='2 6'
pat_start_finish[4]='2 6'
pat_start_finish[5]='2 7'
pat_start_finish[6]='2 7'
pat_start_finish[7]='2 13'
pat_start_finish[8]='2 13'

good_bad_thres[1]='1 1 1'
good_bad_thres[2]='1 2 1'
good_bad_thres[3]='1 1 1'
good_bad_thres[4]='1 4 1'
good_bad_thres[5]='1 1 1'
good_bad_thres[6]='1 6 1'
good_bad_thres[7]='1 4 1'
good_bad_thres[8]='1 8 1'


# Erzeuge leere Startmuster, lösche Datei mit patgen-Parametern.
rm -f $1.0 $1.rules
touch $1.0

for i in 1 2 3 4 5 6 7 8; do

  # Erzeuge Muster des aktuellen Levels.  Steuereingaben werden patgen
  # mittels einer Pipe übergeben.
  echo "patgen $1.dict $1.$(($i-1)) $1.$i $2"
  printf "%s\n%s\n%s\n%s" "${hyph_start_finish[$i]}" \
                          "${pat_start_finish[$i]}" \
                          "${good_bad_thres[$i]}" \
                          "y" \
  | patgen $1.dict $1.$(($i-1)) $1.$i $2 \
  | tee $1.$i.log

  # Sammle verwendete patgen-Parameter in Datei.
  printf "%%   %s | %s | %s\n" "${hyph_start_finish[$i]}" \
                               "${pat_start_finish[$i]}" \
                               "${good_bad_thres[$i]}" \
  >> $1.info

done

rm pattmp.[1-8]

echo -n "\patterns{" > $1.pat
cat $1.8 >> $1.pat
echo "}" >> $1.pat

# eof
