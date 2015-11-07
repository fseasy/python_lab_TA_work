// localEval.cpp : 定义控制台应用程序的入口点。
//

#include "stdafx.h"

using namespace std ;


BOOL WriteSamples(const HANDLE & hParentWrite , char * sample)
{
    BOOL bRet = FALSE ;
    DWORD dwWritten ;
    DWORD dwSize = strlen(sample) ;
    bRet = WriteFile(hParentWrite , sample , dwSize , &dwWritten , NULL) ;
    //cerr << "write to proces " << dwWritten << "Bytes" << endl ;
    return bRet ;
}

BOOL ReadData(const HANDLE & hParentRead , char * data )
{
    DWORD dwRead ;
    // ReadFile 会造成阻塞！！
    BOOL bRet = ReadFile(hParentRead , data , 1024 , &dwRead , NULL) ;
    //cout << "read!" << endl ;
    if(dwRead != 0)
    {
        //cerr << "read data from process " << dwRead << endl ;
    }

    return bRet ;
}


BOOL GetCodeRunResult(char * filePath , char *sample , char  data[])
{
    const int MAX_SIZE = 1024 ;
    char exeCommands[MAX_SIZE] = "cmd /c python " ;
    strcat(exeCommands , filePath) ;
    TCHAR pyFilePath[MAX_SIZE] ;

    swprintf(pyFilePath,L"%S", exeCommands);

    HANDLE hParentWrite , hChildRead ;
    HANDLE hParentRead , hChildWrite ;
    HANDLE hChildErrWrite ;

    STARTUPINFO siStartInfo ;
    PROCESS_INFORMATION piProcInfo ;

    SECURITY_ATTRIBUTES sa;
    sa.nLength = sizeof(SECURITY_ATTRIBUTES);
    sa.lpSecurityDescriptor = NULL;
    sa.bInheritHandle = TRUE;

    BOOL bRet = CreatePipe(&hParentRead , &hChildWrite , &sa , 0) ;
    if(!bRet)
    {
        cerr << "Failed to create read pipe" << endl ;
        return -1 ;
    }
    bRet = CreatePipe(&hChildRead , &hParentWrite , &sa, 0) ;
    if(!bRet)
    {
        cerr << "Failed to ceate write pipe" << endl ;
        return -1 ;
    }
    bRet = DuplicateHandle(GetCurrentProcess() , hChildWrite , GetCurrentProcess() , &hChildErrWrite , 0 , TRUE , DUPLICATE_SAME_ACCESS) ;
    if(!bRet)
    {
        cerr << "Failed to create cerr pipe" << endl ;
        return -1 ;
    }

    siStartInfo.cb = sizeof(STARTUPINFO) ;
    GetStartupInfo(&siStartInfo) ;

    siStartInfo.wShowWindow = SW_HIDE;
    siStartInfo.dwFlags = STARTF_USESHOWWINDOW | STARTF_USESTDHANDLES;
    siStartInfo.hStdOutput = hChildWrite ;
    siStartInfo.hStdInput = hChildRead ;
    siStartInfo.hStdError = hChildErrWrite ;


    bRet = CreateProcess(NULL  ,
                         pyFilePath,
                         NULL ,
                         NULL ,
                         TRUE ,
                         NULL ,
                         NULL ,
                         NULL ,
                         &siStartInfo ,
                         &piProcInfo ) ;
    if(!bRet)
    {
        cerr << "Failed to create process ." << endl ;
        return -1 ;
    }
    bRet = WriteSamples(hParentWrite , sample) ;
    if(!bRet)
    {
        cerr << "Failed to write data to process ." << endl ;
        return -1 ;
    }
    WaitForSingleObject(piProcInfo.hProcess , 10 * 1000) ; // maximun wait 2000 milliseconds
    ZeroMemory(data , 1024) ;
    bRet = ReadData(hParentRead , data) ;
    if(!bRet)
    {
        cerr << "Failed to Read data from process ." << endl ;
        return -1 ;
    }
    CloseHandle(hParentRead) ;
    CloseHandle(hParentWrite) ;
    CloseHandle(hChildRead) ;
    CloseHandle(hChildWrite) ;
    CloseHandle(hChildErrWrite) ;
}

BOOL EvalResult(char * codeRst , char * sampleRst)
{
    string codeRstStr(codeRst) ;
    string sampleRstStr(sampleRst) ;
    clearAllSpaceChar(codeRstStr) ;
    clearAllSpaceChar(sampleRstStr) ;
    //cout << codeRstStr << endl ;
    //cout << sampleRstStr << endl ;
    return ( codeRstStr == sampleRstStr ) ? TRUE : FALSE ;
}

int _tmain(int argc, _TCHAR* argv[])
{


    // ------------ start logic --------------
    char samplesIn[2][256] = {"7-111-18777-6\n"
                              "0-0000-0300-x\n"
                              "0-0000-0300-X\n"
                              "$$$\n"
                              ,
                              "9900-99910-1\n"
                              "99--9999140-9\n"
                              "7-1x1-18777-9\n"
                              "7-111-18777-A\n"
                              "7-111-1877-7x\n"
                              "7-111-189-x\n"
                              "$$$\n"
                             } ;
    char samplesOut[2][256] =
    {
        "Valid ISBN\n"
        "Valid ISBN\n"
        "Valid ISBN\n"
        ,
        "Invalid ISBN Format\n"
        "Invalid ISBN Format\n"
        "Invalid ISBN Format\n"
        "Invalid ISBN Format\n"
        "Invalid ISBN Format\n"
        "Invalid ISBN Format\n"
    } ;

    char wrongTips[2][256] = 
    {
        "正确的ISBN" ,
        "格式不对的ISBN或校验不对的ISBN" 
    } ;
    cout << "\n===========ISBN本地测试===========\n" ;
    cout << "请输入Python代码文件完整路径（可在文件浏览器中打开，然后拖动文件图标到该控制台界面）:\n" ;
    char filePath[1024] ;
    cin >> filePath ;
    char data[1024] ;
    for(size_t i = 0 ; i < 2 ; ++i)
    {
        GetCodeRunResult(filePath , samplesIn[i] , data) ;
        BOOL bEvalResult = EvalResult(data , samplesOut[i]) ;
        cout << "第" << i+1 << "个测试用例结果：" ;
        if(bEvalResult)
        {
            cout << "正确" << endl ;
        }
        else
        {
            cout << "错误" << endl ;
            cout << "\t错误反馈：" <<wrongTips[i] << endl ;
        }
    }

    //cout << "finished" << ; ;

    system("pause") ;
    return 0;
}

