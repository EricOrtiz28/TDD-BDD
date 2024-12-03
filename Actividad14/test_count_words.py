# test_count_words.py

from count_words import CountWords

#Ruta 1
def test_two_words_ending_with_s():
    words = CountWords().count("dogs cats")
    assert words == 2

#Ruta 2
def test_no_words_at_all():
    words = CountWords().count("dog cat")
    assert words == 0

#Ruta 3
def test_words_that_end_in_r():
    words = CountWords().count("car bar")
    assert words == 2

#Ruta 4
def test_word_ending_with_s_at_end():
    words = CountWords().count("cats")
    assert words == 1

#Ruta 5
def test_mixed_endings():
    words = CountWords().count("car cats")
    assert words == 2

#Ruta 6
def test_non_alpha_characters():
    words = CountWords().count("dogs, cats.")
    assert words == 2

#Ruta 7
def test_empty_string():
    words = CountWords().count("")
    assert words == 0

#Ruta 8
def test_only_non_alpha():
    words = CountWords().count("!!!")
    assert words == 0

#Ruta 9
def test_only_s():
    words = CountWords().count("s")
    assert words == 0

#Ruta 10 
def test_only_n():
    words = CountWords().count("r")
    assert words == 0

#Ruta 11
def test_not_words():
    words = CountWords().count(".s")
    assert words == 0

#Ruta 12
def test_apos():
    words = CountWords().count("master's car")
    assert words == 2

#Ruta 13
def test_word_with_apostrophe_in_different_position():
    words = CountWords().count("cat's dog's bar")
    assert words == 3