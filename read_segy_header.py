# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 21:49:22 2018

@author: Aiiluo
"""
import struct
class segyheader():
    
#    I use this class to define some information about segy format,
#    like the trace header lens in segy data.
#    Use the module like this:
#        
#    >>> header = Segy_header()
#    >>> header.read_segy_file(file_full_name)
#    >>> header.read_text_header()
#    ...
    
    
    def __init__(self,inline=41,i_lens=4,i_fmt='i',xline=45,\
                 xl_lens=4,xl_fmt='i',cdpx=193,X_lens=4,X_fmt='i',\
                 cdpy=197,Y_lens=4,Y_fmt='i'):
#   To define some important parameters in segy header
#    Define the position of inline,xline,cpd_x,cpd_y in segy trace header,because each segy data have it's own standard.
#    You have to define this before you read segy data.
        self.text_header_lens = 3200
        self.bin_header_lens = 400
        self.trace_header_lens = 240
        self.inline_position = inline
        self.ilens = i_lens
        self.ifmt = i_fmt
        self.xline_position = xline
        self.xllens = xl_lens
        self.xlfmt = xl_fmt
        self.cdp_x = cdpx
        self.Xlens = X_lens
        self.Xfmt = X_fmt
        self.cdp_y = cdpy
        self.Ylens = Y_lens
        self.Yfmt = Y_fmt
        
        
    
    def read_segy_file(self,address):
#    read the full address of segy data    
        self.segy_file = address
        
        
    def EBCDIC2ASCII(self,ebc_input): 
#   定义ECBDIC转ASCII的字典
        dict = [
                'NUL','SOH','STX','ETX','SEL','HT','RNL','DEL','GE','SPS','RPT','VT','FF','CR','SO','SI',
                'DLE','DC','DC','DC','RE','NL','BS','POC','CAN','EM','UBS','CU','IFS','IGS','IRS','IUSIT',
                'DS','SOS','FS','WUS','BYP','LF','ETB','ESC','SA','SFE','SMS','CSP','MFA','ENQ','ACK','BEL',
                ' ',' ','SYN','IR','PP','TRN','NBS','EOT','SBS','IT','RFF','CU','DC','NAK',' ','SUB',
                ' ','RSP',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','<','(','+','|',
                '&',' ',' ',' ',' ',' ',' ',' ',' ',' ','!','$','*',')',';','&not',
                '-','/',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','%','_','>','?',
                ' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',':','#','@',' ','=','"',
                ' ','a','b','c','d','e','f','g','h','i',' ',' ',' ',' ',' ','+_',
                ' ','j','k','l','m','n','o','p','q','r',' ',' ',' ',' ',' ',' ',
                ' ','~','s','t','u','v','w','x','y','z',' ',' ',' ',' ',' ',' ',
                '^',' ',' ',' ',' ',' ',' ',' ',' ',' ','[',']',' ',' ',' ',' ',
                '{','A','B','C','D','E','F','G','H','I','SHY',' ',' ',' ',' ',' ',
                '}','J','K','L','M','N','O','P','Q','R',' ',' ',' ',' ',' ',' ',
                ' ',' ','S','T','U','V','W','X','Y','Z',' ',' ',' ',' ',' ',' ',
                '0','1','2','3','4','5','6','7','8','9',' ',' ',' ',' ',' ','EO',
                ]
        int_ebc = int(ebc_input)
        asc_output = dict[int_ebc]
        return asc_output

#    def trace_header_position(self,inline=41,i_lens=4,i_fmt='i',xline=45,\
#                          xl_lens=4,xl_fmt='i',cdpx=193,X_lens=4,X_fmt='i',\
#                          cdpy=197,Y_lens=4,Y_fmt='i'):
##    Define the position of inline,xline,cpd_x,cpd_y in segy trace header,because each segy data have it's own standard.
##    You have to define this before you read segy data.
#        self.inline_position = inline
#        self.ilens = i_lens
#        self.ifmt = i_fmt
#        self.xline_position = xline
#        self.xllens = xl_lens
#        self.xlfmt = xl_fmt
#        self.cdp_x = cdpx
#        self.Xlens = X_lens
#        self.Xfmt = X_fmt
#        self.cdp_y = cdpy
#        self.Ylens = Y_lens
#        self.Yfmt = Y_fmt

    
    def read_text_header(self):
#    Read EBCDIC or ASCII data in fisrt 3200 bytes data in segy.
        asc = [0] * self.text_header_lens
        asc_line = [0] * (self.text_header_lens + 40)
        m = 0
        with open(self.segy_file,'rb') as in_file:
            in_file.seek(0)
            data = in_file.read(self.text_header_lens)
            if data[0] == 195:
                print("=================== EBCDIC Header====================\n")
                for i in range(0,self.text_header_lens):
                    asc[i] = self.EBCDIC2ASCII(data[i])
            else:
                print("=================== ASCII Header====================\n")
                asc = data
            
        for j in range(0,self.text_header_lens,80):        
            for k in range(0,80):
                asc_line[j+k+m] = asc[j+k]
            asc_line[j+k+m+1] = '\n'
            m = m + 1
        asc_str = ''.join(asc_line)  
        print(asc_str)
    
    def recongnition_fmt(self,fmt_header): 
#   Input the header format in segy binary header and output the name of the format.      
        if fmt_header == 1:
            return "IBM float(4 bytes)"
        elif fmt_header == 2:
            return "Integer(4 bytes)"
        elif fmt_header == 3:
            return "Integer(2 bytes)"
        elif fmt_header == 5:
            return "IEEE float(4 bytes)"
        elif fmt_header == 8:
            return "Integer(1 bytes)"
        else:
            return "This format is no use now."
    
    def amplitude_recover(self,fmt_header):
#    Input the code of amplitude recover and output the name of it.
        if fmt_header == 1:
            return "None"
        elif fmt_header == 2:
            return "Spherical Spreading"
        elif fmt_header == 3:
            return "AGC"
        else:
            return "Others"

    
    def Judge_data_fmt_lens(self,data_fmt):
#   Input the header format in segy binary header and output the bytes lens of the segy file.  
        if (data_fmt == 1) or (data_fmt == 2) or (data_fmt == 5):
            return 4
        elif data_fmt == 3:
            return 2
        else:
            return 1    
        
       
    def read_binary_header(self):
#    read the 400 byte lens binary data in 3201-3260.
        with open(self.segy_file,'rb') as in_file:
            in_file.seek(self.text_header_lens)    
            data = in_file.read(self.bin_header_lens)    
        bin_header = struct.unpack('>3i24h340x',data)
        print("\n=================== Binary Header====================")
        # print(bin_header)        
        print("Line Number:",bin_header[1])    
        print("Sample Intervel:",bin_header[5])
        self.sample_intervel = bin_header[5]
        print("Number of Interval:",bin_header[7])
        self.sample_point = bin_header[7]
        print("Format:",self.recongnition_fmt(bin_header[9]))
        self.data_fmt = bin_header[9]
        print("Gain method:",self.amplitude_recover(bin_header[24]))
        return self.sample_point
    
    def init_binary_header(self):
        
#        Init three parameters:Sample intervel,sample point,sample format(The bytes lens of the wava data).
        
        with open(self.segy_file,'rb') as in_file:
            in_file.seek(self.text_header_lens)    
            data = in_file.read(self.bin_header_lens)    
        bin_header = struct.unpack('>3i24h340x',data)
   
        self.sample_intervel = bin_header[5]
        self.number_of_sample = bin_header[7]
        self.sample_fmt = self.Judge_data_fmt_lens(bin_header[9])    
        self.data_fmt = bin_header[9]
        return self.number_of_sample, self.sample_intervel

    def seek_data_and_read(self,in_file,offset,DataBytes,DataType,whence=0):
#        Int16 -- DataType= 'h'
#        Int32 -- DataType= 'i'
        
        if DataType == 'h':
            fmt = '>' + str(int(DataBytes/2)) + 'h'
        elif DataType == 'i':
            fmt = '>' + str(int(DataBytes/4)) + 'i'
        elif DataType == 'f':
            fmt = '>' + str(int(DataBytes/4)) + 'f'
        else:
            print("====================================================================\n\
                  Wrong format!\nIf header is int16 please input'h',elif input 'i'or'b'.\
                  \n====================================================================")
        in_file.seek(offset,whence)
        data = in_file.read(DataBytes)
        num = struct.unpack(fmt,data)
        return num[0]   
            
    def read_control_file(self,trace='1'):

#        In this function,we can init the control file and then use it to read the seismic data in numpy metrix.
#        For the purpose,you should input some parameters like this:
#            inline_position,is the position of the Inline writed in segy,ifmt,is the format of the data
#            (int32,input'i';int16,input'h';float,input'f')
#            Others parameters is by analogy...
#            ......

        self.init_binary_header()        
        start_num = 3599+(self.number_of_sample*self.sample_fmt+self.trace_header_lens)*(trace-1)
        with open(self.segy_file,'rb') as in_file:            
            Inline =  self.seek_data_and_read(in_file,start_num+self.inline_position,self.ilens,self.ifmt)
            Xline =  self.seek_data_and_read(in_file,start_num+self.xline_position,self.xllens,self.xlfmt)
            Coor_X =  self.seek_data_and_read(in_file,start_num+self.cdp_x,self.Xlens,self.Xfmt)
            Coor_Y =  self.seek_data_and_read(in_file,start_num+self.cdp_y,self.Ylens,self.Yfmt)
#            Number_of_sample = self.seek_data_and_read(in_file,start_num+115,2,'h')
#            Sample_intervel = self.seek_data_and_read(in_file,start_num+117,2,'h')
#            Sample_fmt = self.Judge_data_fmt_lens(self.seek_data_and_read(in_file,3224,2,'h'))
#        print("\n=================== Trace:",trace,"====================")            
#        print('Inline:',Inline)
#        print('CrossLine:',Xline)
#        print('Coordinate X:',Coor_X)
#        print('Coordinate Y:',Coor_Y)
#        print('Number of sample:',Number_of_sample)
#        print('Sample Intervel:',Sample_intervel)
        return (Inline,Xline,Coor_X,Coor_Y) 
    

   
    def read_last_trace_header(self):
        self.init_binary_header()
        start_num = -(self.number_of_sample*self.sample_fmt)-self.trace_header_lens-1
        with open(self.segy_file,'rb') as in_file:
            Inline =  self.seek_data_and_read(in_file,start_num+self.inline_position,self.ilens,self.ifmt,2)
            Xline =  self.seek_data_and_read(in_file,start_num+self.xline_position,self.xllens,self.xlfmt,2)
            Coor_X =  self.seek_data_and_read(in_file,start_num+self.cdp_x,self.Xlens,self.Xfmt,2)
            Coor_Y =  self.seek_data_and_read(in_file,start_num+self.cdp_y,self.Ylens,self.Yfmt,2)
        
        return (Inline,Xline,Coor_X,Coor_Y)



            
        
            
    

            
            


 

    
