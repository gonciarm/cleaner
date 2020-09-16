import os, shutil
from datetime import date

def main():
    path = os.path.dirname(os.path.realpath(__file__))#grabs directory/path where script file is present
    os.chdir(path)#changes working directory to path
    
    #Configuration: key=subfolders, values = list of file extensions base on which files will be moved to the target subdirectories during cleanup, add as many as you want and change names
    #Sample configuration below
    config = {
        "spreadsheets": ["xls", "xlsx", "csv", "xlsm", "xlsb", "xltx", "xltm", "xlt", "xlam", "xla", "xlw", "xlr"],
        "images": ["png", "jpg", "bmp", "jpeg", "gif", "tiff", "raw", "svg", "exif"],
        "docs": ["doc", "docm", "docx", "dot", "dotx", "pdf", "pot", "potm", "potx", "ppam", "pps", "ppsm", "ppsx", "ppt", "pptm", "pptx", "rtf", "txt"],
        "audio": ["mp3", "wma", "m4a", "flac", "aac", "ogg", "wav", "aiff", "alac"], 
        "archives": ["zip", "rar", "tar", "7z", "ace"],
        "video": ["avi", "mkv", "mp4", "mpg", "mpeg", "wmv", "rmvb"]
    }
        
    def filesList(path): #Creates list of files, excluding directories located in path 
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        return files
     
    def finalFiles(list1, list2):
        listOfFinalFiles = []
        for i in list1:
            if i not in list2:
                listOfFinalFiles.append(i) 
        return listOfFinalFiles

    def extCheck(configurationDict): #creates subdirectories list bease on config where subdirectory = key
        keyList = []
        for key in configurationDict.keys():
            keyList.append(key)
        return  keyList

    def filesNotMoved(file): #creates lis of not moved files
        alreadyExist.append(file)
        return alreadyExist
    
    #Main flow
    uniqueExtensions = []
    filesExtensions = []
    alreadyExist = []
    initialFilesList = filesList(path) #variable storing list of files in the cleaning directory before cleanup
    initFilesCount = len(filesList(path)) #variable storing number of files in the directory before cleaning, used in log file
    
    for file in initialFilesList:
        extension = os.path.splitext(file)[1][1:] #slices file extension
        filesExtensions.append(extension.lower()) #extension assignment  to filesExtensions list
        if extension not in uniqueExtensions and extension !="": #check if extension is unique and exist
                uniqueExtensions.append(extension.lower()) #unique extension assignment  to uniqueExtensions list
    
    fileWithExtension = dict(zip(filesList(path),filesExtensions)) #from two lists creates dictionary where: key = full filename, value = file extension
    
    for extension in uniqueExtensions: #creates the subdirectories based on extension of files directory
            for i in extCheck(config):
                if extension in config[i]:
                    try:
                     os.mkdir(i)
                    except:
                        pass

    #file cleanup
    for element in initialFilesList: 
        for extension in extCheck(config):
            if fileWithExtension[element] in config[extension]:
                src = os.path.realpath(element)
                dst = path + "\\"+ extension
                try:
                    shutil.move(src, dst)
                except shutil.Error:
                    filesNotMoved(element)                    

    finalFilesList = filesList(path)#variable storing list of files in directory after cleanup, for log file
    notRecognized = finalFiles(finalFilesList, alreadyExist)#variable storing list of files without extension or extension not added to configuration

    # Creates log file
    filesNotMoved  = len(filesList(path))#variable storing number of files left in directory after cleanup
    filesMoved = initFilesCount -  filesNotMoved#variable storing number of files moved to subdirectories after cleanup
    timestamp = date.today().strftime('%Y-%m-%d')
    with open(f'cleanerLog_{timestamp}.txt', 'w') as f:
        f.write(f"Files found in directory: {initFilesCount}\nFiles moved to subdirectories: {filesMoved}\nFiles not moved: {filesNotMoved}\n\nFiles that were not moved:\n")
        for element in notRecognized:
            f.write(f"{element}\t\t(reason: file extension not recognized)\n")
        for file in alreadyExist:
            f.write(f"{file}\t\t(reason: file already exist in target directory)\n")
            
if __name__ == "__main__":
    main()