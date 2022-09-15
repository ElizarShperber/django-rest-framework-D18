from django import template


register = template.Library()


list_bad_words = ['редиска', 'пидорас', 'хуй']


@register.filter()
def censor(text):

   # пустой список куда будут падать очищенные слова
   list_output = []

   # делим пришедший текст по пробелу и делаем список
   word_list = text.split()


   # каждое слово из списка проверяем если оно в списке плохих слов
   for word in word_list:
      if word in list_bad_words:
         word = '***'

      # очищенное слово кидаем в список на выход
      list_output.append(word)

   # очищенный список превращаем в строку
   text_output = ' '.join(list_output)

   return text_output