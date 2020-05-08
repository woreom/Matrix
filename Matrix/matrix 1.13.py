'''


This application will compute the reverse matrix of a matrix with and without determinant
of it.

In order to make the reverse matrix we have to be able to make a a matrix's minor and its
transpose but because of lack of many functions in the class we also added many functions
like multiplication of to matrix ,determinant corectify add function and __str__ and also
rewrote most of the functions in the class.

'''



from copy import deepcopy as copy
class Matrix:
    
    def __init__(self, rows):
        self.rows = copy(rows[::])
        self.m = len(rows)
        try:
            self.n = len(rows[0])
        except IndexError:
            self.n = 0
        for i in range(len(rows)):
            if self.n != len(rows[i]):
                raise Exception('The lenth of every row most be equal')
            
    def __rmul__(self, c): #scalar product from right
        C=()
        for row in self.rows:
            r=()
            for i in row:
                r+=(i*c,)
            C+=(list(r),)
        return Matrix(list(C))
    
    def __mul__(self, other): #scalar product from left
        C=()
        for row in self.rows:
            r=()
            for i in row:
                r+=(i*c,)
            C+=(list(r),)
        return Matrix(list(C))
    def __add__(self, M): #add function
        assert self.m == M.m and self.n == M.n
        C = ()
        for i in range(self.m):
            row =()
            for j in range(self.n):
                row += (self.rows[i][j] + M.rows[i][j],)
            C += (list(row),)
        return Matrix(list(C))

    def __eq__(self,other):
        if self.rows==other.rows :
            return True
        return False

    def __str__(self):
        Max=''
        for i in self.rows:
            for j in i:
                if len(Max)<len(str(j)):
                    Max=str(j)
        n=len(Max)
        string = ""
        for i in range(self.m):
            s="\x05"
            for j in range(self.n):
                s += str(self.rows[i][j])+' '*(n+1-len(str(self.rows[i][j])))
                #if j != self.n - 1: s += ' '*(n+1-len(str(self.rows[i][j])))
            s+="\x05\n"
            string += s
        return string

    def prod(self, M):
            assert self.n == M.m
            C = ()
            for i in range(self.m):
                row = ()
                for j in range(M.n):
                    result = 0
                    for k in range(self.n):
                        result += self.rows[i][k] * M.rows[k][j]
                    row += (result,)
                C += (list(row),)
            return Matrix(list(C))

    def det(self):
        if self.m ==1and self.n ==1:
            return self.rows[0][0]
        if self.m ==2 and self.n ==2:
            return (self.rows[0][0]*self.rows[1][1])-(self.rows[0][1]*self.rows[1][0])
        temp=copy(self.rows[1:])
        result=0
        for i in range(self.n):
            r=[]
            for j in range(self.m-1):
                r.append(temp[j][:i]+temp[j][i+1:])
            result+= (-1)**i * self.rows[0][i] * Matrix(r).det()
        return result

    def matrix_transpose(self):
        '''This functions simply changes the place of each row with each column.'''
        all_columns=[]
        n=len(self.rows[0])
        for j in range(n):
            column=[]
            for i in self.rows:
                column.append(i[j])
            all_columns.append(column)
        return Matrix(all_columns)

    def clairfy(self):
        C=()
        for row in self.rows:
            t=()
            for i in range(self.n):
                if row[i]>=-0.001 and row[i]<=0.001:
                    t+=(0.0,)
                else:
                    t+=(row[i],)
            C+=(list(t),)
        return Matrix(list(C))
    
    def one_row_scalar_prod(self,c, num_row):
        rows=[]
        for i in range(self.m):
            rows.append(list(self.rows[i]))
        for i in range(self.n):
            rows[num_row][i]= rows[num_row][i]*c
        return Matrix(rows)
    
    def change_rows(self, rows_index):
        rows=[]
        for i in rows_index:
            rows.append(self.rows[i])
        return Matrix(rows)
    
    def change_i_j_row(self,num_row1,num_row2):
        rows=[]
        for i in range(self.m):
            rows.append(list(self.rows[i]))
        rows[num_row1],rows[num_row2]=rows[num_row2], rows[num_row1]
        return Matrix(rows)
        
    def combine(self,c,num_row1, num_row2):
        rows=[]
        for i in range(self.m):
            rows.append(list(self.rows[i]))
        for i in range(self.n):
            rows[num_row2][i] += c*rows[num_row1][i]
        return Matrix(rows)
            
    def identity(self):
        newTup=[]
        for i in range(self.m):
            newRow=[]
            for j in range (self.n):
                if i==j:
                    newRow.append(1)
                else:
                    newRow.append(0)
            newTup.append(newRow)
        return Matrix(newTup)
        

    def count0(self):
        import operator
        dic={}
        for i in range(self.m):
            counter=0
            for j in range(self.n):
                if self.rows[i][j]==0:
                    counter+=1
                else: break;
            dic[i]=counter
        dic = sorted(dic.items(), key=operator.itemgetter(1))
        return dic

    def organize(self):
        a=self.count0()
        rowsIndex=[]
        rows=[]
        for i in range(self.m):
            rowsIndex.append(a[i][0])
            rows.append(self.rows[a[i][0]])
        way_of_echelon.append(["change_rows",rowsIndex])
        return Matrix(rows)


    def make_up_triangle(self):
        if self.m==self.n:
            m=self.m
            n=self.m
        else:
            if self.m<self.n:
                m=self.m
                n=m
            else:
                m=self.n
                n=m+1
        rows=copy(self.rows)
        M=Matrix(rows)
        for i in range(m):
            a=M.rows[i][i]
            if a!=0:
                for k in range(i+1,n):
                    b=M.rows[k][i]
                    way_of_echelon.append(["make_up_triangle",[b*-1.0/a, i, k]])
                    M=M.combine(b*-1.0/a, i, k)
##                    print M
                M=M.organize()
##        print M
        return M
        
    def make_down_triangle(self):
        if self.m<self.n:m=self.m
        else:m=self.n
        rows=copy(self.rows)
        M=Matrix(rows)
        for i in range(m):
            a=M.rows[i][i]
            if a!=0:
                for k in range(i):
                    b=M.rows[k][i]
                    way_of_echelon.append(["make_down_triangle",[b*-1.0/a, i, k]])
                    M=M.combine(b*-1.0/a, i,k)
##                    print M
                M=M.organize()
##        print M
        return M
        
    def make_echelon(self):
            global way_of_echelon
            way_of_echelon=[]
            M=self.make_up_triangle()
            M=M.make_down_triangle()
            if M.m<=self.n: m=M.m
            else: m=M.n
            for i in range(m):
                if M.rows[i][i]!=0:
                    way_of_echelon.append(["one_row_scalar_prod",[1.0/M.rows[i][i],i]])
                    M=M.one_row_scalar_prod(1.0/M.rows[i][i],i)
            M=M.make_up_triangle()
            M=M.make_down_triangle()
    ##        print M
            return M.clairfy()
         
    def solve(self,other):
        self.make_echelon().clairfy()
##        print copy(other.rows)
        M=Matrix(copy(other.rows))
##        print M
        counter=-1
        for i in way_of_echelon:
            if i[0]=="one_row_scalar_prod":
                M=M.one_row_scalar_prod(i[1][0],i[1][1])
##                if i[1][0]<0 : print 1
            elif i[0]=="make_down_triangle":
                M=M.combine(i[1][0],i[1][1],i[1][2])
            elif i[0]=="make_up_triangle":
                M=M.combine(i[1][0],i[1][1],i[1][2])
            elif i[0]=="change_rows":
##                print str(i[1][0]) + " , " + str(i[1][1])
                M=M.change_rows(i[1])
##            print M
        return M
        

    
class SquareMatrix(Matrix):

    def __init__(self, rows):
        Matrix.__init__(self, rows)
        if self.m != self.n:
            raise Exception('The len(rows) most be equal to len(columes)')
        
    def delete_irow_jcolume(self,i,j):
        temp=copy(self.rows[:i]+self.rows[i+1:])
        t=()
        for row in temp:
            row=row[:j]+row[j+1:]
            t+=(row,)
        return SquareMatrix(t)

    def matrix_minor(self):
        '''This function is the minor matrix of a matrix which each cell of minor matrix is determinant
        of the matrix that will appear when we emit the cell's row and column multiply by the value of the cell. '''
        C=()
        for i in range(self.m):
            t=()
            for j in range(self.n):
                M=self.delete_irow_jcolume(i,j)
                a=((-1)**(i+j))*M.det()
                t+=(a,)
            C+=(list(t),)
        return SquareMatrix(list(C))
        
    def  reverse(self):
        a=self.det()
        T=self.matrix_minor()
        return(1.0/a)*(T.matrix_transpose())
    
    def reverse1(self):
##        assert make_echelon()==(self.identity())
        M=self.solve(self.identity()).clairfy()
        return M
        
        

        
    
    
                
                

if __name__ == "__main__":
    a=SquareMatrix([[0,2,0,1,0],[6,1,0,2,1],[8,10,5,3,6],[1,2,3,4,3],[1,2,11,23,111]])
    print "The Matrix :"
    print a
    print "reversed without determinant :"
    M1=a.reverse1()
    print M1
    print M1.prod(a).clairfy()
    print "reversed with determinant :"
    M2=a.reverse().clairfy()
    print M2
    print M2.prod(a).clairfy()
    print
    print "-------------------------------------------------------------------------------------------------------------------------------------------------"
    print
    a=SquareMatrix([[2,6],[3,47]])
    print "The Matrix :"
    print a
    print "reversed without determinant :"
    M1=a.reverse1()
    print M1
    print M1.prod(a).clairfy()
    print "reversed with determinant :"
    M2=a.reverse().clairfy()
    print M2
    print M2.prod(a).clairfy()
    print
    print "-------------------------------------------------------------------------------------------------------------------------------------------------"
    print
    a=SquareMatrix([[1,0,0],[0,1,0],[0,0,1]])
    print "The Matrix :"
    print a
    print "reversed without determinant :"
    M1=a.reverse1()
    print M1
    print M1.prod(a).clairfy()
    print "reversed with determinant :"
    M2=a.reverse().clairfy()
    print M2
    print M2.prod(a).clairfy()
    print
    print "-------------------------------------------------------------------------------------------------------------------------------------------------"
    print
    a=SquareMatrix([[1,2,3],[2,4,5],[3,5,6]])
    print "The Matrix :"
    print a
    print "reversed without determinant :"
    M1=a.reverse1()
    print M1
    print M1.prod(a).clairfy()
    print "reversed with determinant :"
    M2=a.reverse().clairfy()
    print M2
    print M2.prod(a).clairfy()
    print
    print "-------------------------------------------------------------------------------------------------------------------------------------------------"
    print    
    a=Matrix([[1,2],[2,3],[3,4]])
    print a
    print a.make_echelon()
    print "-------------------------------------------------------------------------------------------------------------------------------------------------"
    print    
    a=Matrix([[1,2,3],[3,4,5]])
    print a
    print a.make_echelon()
