def progress_bar(current, total, min_remaining, bar_length=50):
    fraction = current / total

    arrow = int(fraction * bar_length - 1) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '

    ending = '\n' if current == total else '\r'

    print(f'PROGRESS: [{arrow}{padding}] {int(fraction*100)}% //', min_remaining, 'minutes remaining', end=ending)
    
    return



def progress_bar_pct_only(current, total, bar_length=50):
    fraction = current / total

    arrow = int(fraction * bar_length - 1) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '

    ending = '\n' if current == total else '\r'

    print(f'PROGRESS: [{arrow}{padding}] {int(fraction*100)}%', end=ending)