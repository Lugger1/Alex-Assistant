import wikipedia
from scripts import load_show, modif_thread

err = False

def search(data:str) -> str:
    global err
    wikipedia.set_lang('ru')
    
    thr = modif_thread.thread_with_exception(func=load_show.show_load, name='scearch')
    thr.start()
    
    try:
        a = wikipedia.summary(data)

    except wikipedia.exceptions.DisambiguationError as err:
        a = 'Уточните поиск информации'
        err = True
        load_show.status = False

    finally:
        load_show.status = False
        thr.raise_exception()
    
    return a
