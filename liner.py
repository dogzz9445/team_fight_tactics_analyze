import os
import sys
import datetime
import pandas as pd

def filemtime(df, filename):
    global cnt
    os.chdir(path)
    with open(filename,'r', errors='replace') as f:
        lines = f.readlines()
        for cnt, line in enumerate(lines,1):
            pass
    data = {
        '파일명' : filename,
        '크기' : str(os.path.getsize(filename)),
        '라인수' : str(cnt),
        '생성날짜' : str(datetime.datetime.fromtimestamp(os.path.getctime(filename)).strftime('%Y-%m-%d'))
    }
    df = df.append(data, ignore_index=True)
    
    return df

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('help: liner.exe [input file] [output file]')
        sys.exit()

    filters = ('.otf')   # filter File Name Extension
    rootpath = sys.argv[1]
    outfile = sys.argv[2]


    df = pd.DataFrame(columns=['파일명', '크기', '생성날짜', '라인수'])
    
    for (path, dir, files) in os.walk(rootpath):       # search rootpath
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            if ext in filters:
                pass

            else:
                df = filemtime(df, filename)
                
    df = df.sort_values(by=['파일명'])

    print(df)
    df.to_csv(outfile, encoding='utf-8')