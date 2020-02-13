#include<iostream>
#include<vector>
#include<cstdlib>
#include<cstdio>
#include<cmath>

using namespace std;
class myvec{
    public:
        int moved_temp = 1;
    public:
        myvec () {
        srand(time(NULL));
        }
    public:
        vector <vector<int> > left(vector<vector<int> > vect){
        vector <vector<int> > result;
        int j;
        for(j =0; j< 4; j++){
            vector <int> res;
            int merged = 0;
            int i;
            for(i =3; i>=0; i--){
                int t = vect[j][i];
                if(t==0){continue;}
                int s = res.size();
                if(s > 0 and t == res[s-1] and merged == 0){
                    res[s-1] += t;
                    merged = 1;
                }
                else{
                    if(s> 0){
                        merged = 0;
                     }
                     res.push_back(t);
                    }
                }
            int s = res.size();
            vector <int> pes(s, 0);
            for(int p=0;p<s;p++){
            pes[p] = res[s-p-1];
            }
            for(int p = 0; p < 4 - s; p++){
            pes.push_back(0);
            }
            result.push_back(pes);  
            }
            return result;
        }
    public:
        vector <vector<int> > right(vector<vector<int> > vect){
        vector <vector<int> > result;
        int j;
        for(j =0; j< 4; j++){
            vector <int> res;
            int merged = 0;
            int i;
            for(i =0; i<4; i++){
                int t = vect[j][i];
                if(t==0){continue;}
                int s = res.size();
                if(s > 0 and t == res[s-1] and merged == 0){
                    res[s-1] += t;
                    merged = 1;
                }
                else{
                    if(s> 0){
                        merged = 0;
                     }
                     res.push_back(t);
                    }
                }
            int s = res.size();
            vector <int> pes(4,0);
            int count = 3;
            for(int p = s-1; p>=0;p--){
                pes[count] = res[p];count -= 1;
            }
            result.push_back(pes);
            }
            
            return result;
        }
    public:
        vector <int> l(vector<int> vect){
        vector <int> result;
            vector <int> res;
            int merged = 0;
            int i;
            for(i =3; i>=0; i--){
                int t = vect[i];
                if(t==0){continue;}
                int s = res.size();
                if(s > 0 and t == res[s-1] and merged == 0){
                    res[s-1] += t;
                    merged = 1;
                }
                else{
                    if(s> 0){
                        merged = 0;
                     }
                     res.push_back(t);
                    }
                }
            int s = res.size();
            vector <int> pes(s, 0);
            for(int p=0;p<s;p++){
            pes[p] = res[s-p-1];
            }
            for(int p = 0; p < 4 - s; p++){
            pes.push_back(0);
            }
            result = pes;  
            
            return result;
        }
    public:
        vector <int > r(vector<int > vect){
        vector <int > result;
            vector <int> res;
            int merged = 0;
            int i;
            for(i =0; i<4; i++){
                int t = vect[i];
                if(t==0){continue;}
                int s = res.size();
                if(s > 0 and t == res[s-1] and merged == 0){
                    res[s-1] += t;
                    merged = 1;
                }
                else{
                    if(s> 0){
                        merged = 0;
                     }
                     res.push_back(t);
                    }
                }
            int s = res.size();
            vector <int> pes(4,0);
            int count = 3;
            for(int p = s-1; p>=0;p--){
                pes[count] = res[p];count -= 1;
            }
            result = pes;
            
            
            return result;
        }
    public:
        vector <vector<int> > up(vector<vector<int> > vect){
        vector <vector<int> > result = vect;
        for(int i = 0; i <4;i++){
            vector<int>temp;
            for(int j =0; j<4;j++){
            temp.push_back(vect[j][i]);
            //cout << vect[j][i] << " fsd ";
            }
            vector<int> temp1 = l(temp);
            for(int j =0; j<4;j++){
            result[j][i] = temp1[j];
            }
        }
        return result;
        }
    public:
        vector <vector<int> > down(vector<vector<int> > vect){
        vector <vector<int> > result = vect;
        for(int i = 0; i <4;i++){
            vector<int>temp;
            for(int j =0; j<4;j++){
            temp.push_back(vect[j][i]);
            //cout << vect[j][i] << " fsd ";
            }
            vector<int> temp1 = r(temp);
            for(int j =0; j<4;j++){
            result[j][i] = temp1[j];
            }
        }
        return result;
        }
    public:
        vector <vector<int> > c(vector<vector<int> > vect, int move){
        if(move == 0){ return up(vect);}
        if(move == 1){ return down(vect);}
        if(move == 2){ return left(vect);}
        if(move == 3){ return right(vect);}
        }
    public:
        int isvalid(vector<vector<int> > vect){
            int i, j;
            if(vect[3][3] == 0){return 1;}
            for(i =0; i< 3; i++){
                for(j=0;j<4; j++){
                    if (vect[i][j] == 0){return 1;}
                    if (vect[i][j] == vect[i+1][j]){return 1;}
                }
                if ((vect[i][0] == vect[i][1]) or(vect[i][1] == vect[i][2]) or (vect[i][2] == vect[i][3])){return 1;}
            }
            i = 3;
            for(j=0;j<3;j++){
            if(vect[i][j]==0){return 1;}
            if( vect[i][j] == vect[i][j+1]){ return 1;}
            }
        return 0;
        }
    public:
        int random(int from, int to){
            return rand() % (to - from + 1) + from;
        }
    public:
        vector<vector<int> > fillnum_m(vector<vector<int> > vect1){
            vector<vector<int> > vect = vect1;
            vector<int> indx;
            int t;
            for(int i = 0;i<4;i++){
                for(int j=0;j<4;j++){
                    t = vect[i][j];
                    if(t == 0){indx.push_back(4*i + j);}
                }
            }
            if(vect.size() == 0){ return vect;}
            int m1  = random(0,99) < 90 ? 2:4;
            int num = indx[random(0,indx.size()-1)];
            vect[(int)(num/4)][num%4] = m1;
            return vect;
        }
    public:
        int maxim(vector<vector<int> > vect){
            int m =0;
            for(int i = 0;i<4;i++){
                for(int j=0;j<4;j++){
                    if(m<vect[i][j]){m=vect[i][j];}
                }
            }
            return m;
        }
    public:
        int hasMoved(vector<vector<int> > v1, vector<vector<int> > v2){
            for(int i = 0;i<4;i++){
                for(int j=0;j<4;j++){
                    if(v1[i][j] != v2[i][j]){return 1;}
                }
            }
            return 0;//didn't moved
        }
    public:
        vector<vector<int> > next_play(vector<vector<int> > vect, int move){
            if(move>3 or move<0){return vect;}
            vector<vector<int> > moved_grid = c(vect, move);
            int moved = hasMoved(vect, moved_grid);
            if(moved == 0){moved_temp = 0; return vect;}//return as it was
            moved_grid = fillnum_m(moved_grid);
            return moved_grid;
        }
    public:
            double rand_moves(vector<vector<int> > vect, int first_move, int times){
                int score = maxim(vect);
                vector<vector<int> > vect1;
                vector<vector<int> > vect2 = c(vect, first_move);
                for(int p=0; p<times; p++){
                    vect1 = fillnum_m(vect2);
                    while(isvalid(vect1)==1){
                        vect1 = next_play(vect1, random(0,3));
                        if(moved_temp==0){
                            moved_temp = 1;
                            continue;
                        }
                        score += maxim(vect1);
                    }
                }
                return score/times;
            }
    };






















