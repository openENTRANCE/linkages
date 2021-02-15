clc
clear all

addpath C:\GAMS\win64\24.4

%% export GDX file to matlab

TOTCONS_time.name='TOTCONS_time' 
CONS_H_TT_time.name='CONS_H_TT_time' 
CONS_G_TT_time.name='CONS_G_TT_time' 
INTER_USE_TT_time.name='INTER_USE_TT_time' 
INTER_USE_MM_time.name='INTER_USE_MM_time' 
INTER_USE_DD_time.name='INTER_USE_DD_time' 

CONS_H_M_time.name='CONS_H_M_time' 
CONS_H_D_time.name='CONS_H_D_time' 
CONS_G_M_time.name='CONS_G_M_time' 
CONS_G_D_time.name='CONS_G_D_time' 
GFCF_M_time.name='GFCF_M_time' 
GFCF_D_time.name='GFCF_D_time' 

P_time.name='P_time' 
PK_time.name='PK_time' 
PL_time.name='PL_time' 
GDPCONST_time.name='GDPCONST_time' 

Y_time.name='Y_time' 
X_time.name='X_time' 
K_time.name='K_time' 
L_time.name='L_time'


TOTCONS_time=rgdx('gdx\merged_gdx\merged',TOTCONS_time) 
CONS_H_TT_time=rgdx('gdx\merged_gdx\merged',CONS_H_TT_time) 
CONS_G_TT_time=rgdx('gdx\merged_gdx\merged',CONS_G_TT_time)
INTER_USE_TT_time=rgdx('gdx\merged_gdx\merged',INTER_USE_TT_time)
INTER_USE_MM_time=rgdx('gdx\merged_gdx\merged',INTER_USE_MM_time)
INTER_USE_DD_time=rgdx('gdx\merged_gdx\merged',INTER_USE_DD_time) 



CONS_H_M_time=rgdx('gdx\merged_gdx\merged',CONS_H_M_time)
CONS_H_D_time=rgdx('gdx\merged_gdx\merged',CONS_H_D_time)
CONS_G_M_time=rgdx('gdx\merged_gdx\merged',CONS_G_M_time)
CONS_G_D_time=rgdx('gdx\merged_gdx\merged',CONS_G_D_time)
GFCF_M_time=rgdx('gdx\merged_gdx\merged',GFCF_M_time)
GFCF_D_time=rgdx('gdx\merged_gdx\merged',GFCF_D_time)

P_time=rgdx('gdx\merged_gdx\merged',P_time)
PK_time=rgdx('gdx\merged_gdx\merged',PK_time)
PL_time=rgdx('gdx\merged_gdx\merged',PL_time)
GDPCONST_time=rgdx('gdx\merged_gdx\merged',GDPCONST_time)

X_time=rgdx('gdx\merged_gdx\merged',X_time)
Y_time=rgdx('gdx\merged_gdx\merged',Y_time)
K_time=rgdx('gdx\merged_gdx\merged',K_time)
L_time=rgdx('gdx\merged_gdx\merged',L_time)

%% Understand database

% Data can be found under X_time.val for example

% There are 5 columns to this database. The first 4 columns indicate:
% scenario
% region
% product
% year
% Value
% The last column gives the value that corresponds to this combination 

% Definition of labels in database. This database is in format 'long'.
%X_time.uels{1,1} 
% This has a lenght of 2542 elements
% 1:8 --> regions
% 9:170 --> ind
% 171:174 --> fd
% 176:180 --> unit
% 181:186 --> due
% 187:192 --> ude
% 193:196 --> nature
% 197:204 --> water
% 205:216 --> emis
% 175 & 217:208 --> land
reg_idx=436:465;
ind_idx=482:500;
prd_idx=466:481;
yr_idx=526:565;

% How to find a lost element in this large set of set elements?
%         x= X_time.uels{1,1}
%         %Corresponding unit to this emission type
%         xxx=find(ismember(x,'02_test_H2'));
%         X_time.uels{1,1}{1,2446}
%         X_time.uels{1,1}{1,2447}
%         X_time.uels{1,1}{1,1}


%% X_time
"X_time"

tic
for j=1:size(X_time.val,2)-1
    for i=1:size(X_time.val,1)
        set_idx=X_time.val(i,j);
        stringtable(i,j)=string(X_time.uels{1,1}{1,set_idx}); 
    end
end
toc

X_time_OE(1:size(X_time.val,1),1) = ["EXIOMOD 2.0" ];
X_time_OE(:,2)=stringtable(:,1);
X_time_OE(:,3)=stringtable(:,2);
X_time_OE(:,4)=strcat("Output|Product|",stringtable(:,3));
X_time_OE(:,5)="million euro/yr";
X_time_OE(:,6)=stringtable(:,4);
X_time_OE(:,7)=X_time.val(:,5);

X_time_OE_table = array2table(X_time_OE,...
    'VariableNames',{'Model','Scenario','Region','Variable','Unit','Year','Value'});

X_time_OE_table.Value=str2double(X_time_OE_table.Value);

X_time_OE_table_unstack = unstack(X_time_OE_table,'Value','Year');


%% Y_time
"Y_time"

clear stringtable
tic
for j=1:size(Y_time.val,2)-1
    for i=1:size(Y_time.val,1)
        set_idx=Y_time.val(i,j);
        stringtable(i,j)=string(Y_time.uels{1,1}{1,set_idx}); 
    end
end
toc

Y_time_OE(1:size(Y_time.val,1),1) = ["EXIOMOD 2.0" ];
Y_time_OE(:,2)=stringtable(:,1);
Y_time_OE(:,3)=stringtable(:,2);
Y_time_OE(:,4)=strcat("Output|Industry|",stringtable(:,3));
Y_time_OE(:,5)="million euro/yr";
Y_time_OE(:,6)=stringtable(:,4);
Y_time_OE(:,7)=Y_time.val(:,5);

Y_time_OE_table = array2table(Y_time_OE,...
    'VariableNames',{'Model','Scenario','Region','Variable','Unit','Year','Value'});

Y_time_OE_table.Value=str2double(Y_time_OE_table.Value);

Y_time_OE_table_unstack = unstack(Y_time_OE_table,'Value','Year');

%% K_time
"K_time"

clear stringtable
tic
for j=1:size(K_time.val,2)-1
    for i=1:size(K_time.val,1)
        set_idx=K_time.val(i,j);
        stringtable(i,j)=string(K_time.uels{1,1}{1,set_idx}); 
    end
end
toc

K_time_OE(1:size(K_time.val,1),1) = ["EXIOMOD 2.0" ];           % Model
K_time_OE(:,2)=stringtable(:,1);                                % Scenario
K_time_OE(:,3)=stringtable(:,2);                                % Region
K_time_OE(:,4)=strcat("Capital|",stringtable(:,4));     % Variable
K_time_OE(:,5)="million euro/yr";                               % Unit
K_time_OE(:,6)=stringtable(:,5);                                % Year
K_time_OE(:,7)=K_time.val(:,6);                                 % Value

K_time_OE_table = array2table(K_time_OE,...
    'VariableNames',{'Model','Scenario','Region','Variable','Unit','Year','Value'});

K_time_OE_table.Value=str2double(K_time_OE_table.Value);

K_time_OE_table_unstack = unstack(K_time_OE_table,'Value','Year');

%% PK_time
"PK_time"

clear stringtable
tic
for j=1:size(PK_time.val,2)-1
    for i=1:size(PK_time.val,1)
        set_idx=PK_time.val(i,j);
        stringtable(i,j)=string(PK_time.uels{1,1}{1,set_idx}); 
    end
end
toc

PK_time_OE(1:size(PK_time.val,1),1) = ["EXIOMOD 2.0" ];
PK_time_OE(:,2)=stringtable(:,1);
PK_time_OE(:,3)=stringtable(:,2);
PK_time_OE(:,4)="Capital Price Index|"; % Note mistake with nomenclature
PK_time_OE(:,5)="";
PK_time_OE(:,6)=stringtable(:,3);
PK_time_OE(:,7)=PK_time.val(:,4);

PK_time_OE_table = array2table(PK_time_OE,...
    'VariableNames',{'Model','Scenario','Region','Variable','Unit','Year','Value'});

PK_time_OE_table.Value=str2double(PK_time_OE_table.Value);

PK_time_OE_table_unstack = unstack(PK_time_OE_table,'Value','Year');

%% L_time
"L_time"

clear stringtable
tic
for j=1:size(L_time.val,2)-1
    for i=1:size(L_time.val,1)
        set_idx=L_time.val(i,j);
        stringtable(i,j)=string(L_time.uels{1,1}{1,set_idx}); 
    end
end
toc

L_time_OE(1:size(L_time.val,1),1) = ["EXIOMOD 2.0" ];           % Model
L_time_OE(:,2)=stringtable(:,1);                                % Scenario
L_time_OE(:,3)=stringtable(:,2);                                % Region
L_time_OE(:,4)=strcat("Labor|",stringtable(:,4));     % Variable
L_time_OE(:,5)="million euro/yr";                               % Unit
L_time_OE(:,6)=stringtable(:,5);                                % Year
L_time_OE(:,7)=L_time.val(:,6);                                 % Value

L_time_OE_table = array2table(L_time_OE,...
    'VariableNames',{'Model','Scenario','Region','Variable','Unit','Year','Value'});

L_time_OE_table.Value=str2double(L_time_OE_table.Value);

L_time_OE_table_unstack = unstack(L_time_OE_table,'Value','Year');

%% PL_time
"PL_time"

clear stringtable
tic
for j=1:size(PL_time.val,2)-1
    for i=1:size(PL_time.val,1)
        set_idx=PL_time.val(i,j);
        stringtable(i,j)=string(PL_time.uels{1,1}{1,set_idx}); 
    end
end
toc

PL_time_OE(1:size(PL_time.val,1),1) = ["EXIOMOD 2.0" ];
PL_time_OE(:,2)=stringtable(:,1);
PL_time_OE(:,3)=stringtable(:,2);
PL_time_OE(:,4)="Labor Price Index|"; % Note mistake with nomenclature
PL_time_OE(:,5)="";
PL_time_OE(:,6)=stringtable(:,3);
PL_time_OE(:,7)=PL_time.val(:,4);

PL_time_OE_table = array2table(PL_time_OE,...
    'VariableNames',{'Model','Scenario','Region','Variable','Unit','Year','Value'});

PL_time_OE_table.Value=str2double(PL_time_OE_table.Value);

PL_time_OE_table_unstack = unstack(PL_time_OE_table,'Value','Year');

%% P_time
"P_time"

clear stringtable
tic
for j=1:size(P_time.val,2)-1
    for i=1:size(P_time.val,1)
        set_idx=P_time.val(i,j);
        stringtable(i,j)=string(P_time.uels{1,1}{1,set_idx}); 
    end
end
toc

P_time_OE(1:size(P_time.val,1),1) = ["EXIOMOD 2.0" ];
P_time_OE(:,2)=stringtable(:,1);
P_time_OE(:,3)=stringtable(:,2);
P_time_OE(:,4)=strcat("Price index|",stringtable(:,3)); % Note mistake with nomenclature
P_time_OE(:,5)="";
P_time_OE(:,6)=stringtable(:,4);
P_time_OE(:,7)=P_time.val(:,5);

P_time_OE_table = array2table(P_time_OE,...
    'VariableNames',{'Model','Scenario','Region','Variable','Unit','Year','Value'});

P_time_OE_table.Value=str2double(P_time_OE_table.Value);

P_time_OE_table_unstack = unstack(P_time_OE_table,'Value','Year');

%% GDPCONST_time
"GDPCONST_time"

clear stringtable
tic
for j=1:size(GDPCONST_time.val,2)-1
    for i=1:size(GDPCONST_time.val,1)
        set_idx=GDPCONST_time.val(i,j);
        stringtable(i,j)=string(GDPCONST_time.uels{1,1}{1,set_idx}); 
    end
end
toc

GDPCONST_time_OE(1:size(GDPCONST_time.val,1),1) = ["EXIOMOD 2.0" ];
GDPCONST_time_OE(:,2)=stringtable(:,1);
GDPCONST_time_OE(:,3)=stringtable(:,2);
GDPCONST_time_OE(:,4)="GDP|MER"; % Note mistake with nomenclature
GDPCONST_time_OE(:,5)="million euro/yr";
GDPCONST_time_OE(:,6)=stringtable(:,3);
GDPCONST_time_OE(:,7)=GDPCONST_time.val(:,4);

GDPCONST_time_OE_table = array2table(GDPCONST_time_OE,...
    'VariableNames',{'Model','Scenario','Region','Variable','Unit','Year','Value'});

GDPCONST_time_OE_table.Value=str2double(GDPCONST_time_OE_table.Value);

GDPCONST_time_OE_table_unstack = unstack(GDPCONST_time_OE_table,'Value','Year');

%% CONS_H_M_time
"CONS_H_M_time"

clear stringtable
tic
for j=1:size(CONS_H_M_time.val,2)-1
    for i=1:size(CONS_H_M_time.val,1)
        set_idx=CONS_H_M_time.val(i,j);
        stringtable(i,j)=string(CONS_H_M_time.uels{1,1}{1,set_idx}); 
    end
end
toc

CONS_H_M_time_OE(1:size(CONS_H_M_time.val,1),1) = ["EXIOMOD 2.0" ];
CONS_H_M_time_OE(:,2)=stringtable(:,1);
CONS_H_M_time_OE(:,3)=stringtable(:,3);
CONS_H_M_time_OE(:,4)=strcat("Consumption|Households|",stringtable(:,2),"|Imported");
CONS_H_M_time_OE(:,5)="million euro/yr";
CONS_H_M_time_OE(:,6)=stringtable(:,4);
CONS_H_M_time_OE(:,7)=CONS_H_M_time.val(:,5);

CONS_H_M_time_OE_table = array2table(CONS_H_M_time_OE,...
    'VariableNames',{'Model','Scenario','Region','Variable','Unit','Year','Value'});

CONS_H_M_time_OE_table.Value=str2double(CONS_H_M_time_OE_table.Value);

CONS_H_M_time_OE_table_unstack = unstack(CONS_H_M_time_OE_table,'Value','Year');

%% CONS_H_D_time
"CONS_H_D_time"

clear stringtable
tic
for j=1:size(CONS_H_D_time.val,2)-1
    for i=1:size(CONS_H_D_time.val,1)
        set_idx=CONS_H_D_time.val(i,j);
        stringtable(i,j)=string(CONS_H_D_time.uels{1,1}{1,set_idx}); 
    end
end
toc

CONS_H_D_time_OE(1:size(CONS_H_D_time.val,1),1) = ["EXIOMOD 2.0" ];
CONS_H_D_time_OE(:,2)=stringtable(:,1);
CONS_H_D_time_OE(:,3)=stringtable(:,3);
CONS_H_D_time_OE(:,4)=strcat("Consumption|Households|",stringtable(:,2),"|Domestic");
CONS_H_D_time_OE(:,5)="million euro/yr";
CONS_H_D_time_OE(:,6)=stringtable(:,4);
CONS_H_D_time_OE(:,7)=CONS_H_D_time.val(:,5);

CONS_H_D_time_OE_table = array2table(CONS_H_D_time_OE,...
    'VariableNames',{'Model','Scenario','Region','Variable','Unit','Year','Value'});

CONS_H_D_time_OE_table.Value=str2double(CONS_H_D_time_OE_table.Value);

CONS_H_D_time_OE_table_unstack = unstack(CONS_H_D_time_OE_table,'Value','Year');

%% CONS_G_M_time
"CONS_G_M_time"

clear stringtable
tic
for j=1:size(CONS_G_M_time.val,2)-1
    for i=1:size(CONS_G_M_time.val,1)
        set_idx=CONS_G_M_time.val(i,j);
        stringtable(i,j)=string(CONS_G_M_time.uels{1,1}{1,set_idx}); 
    end
end
toc

CONS_G_M_time_OE(1:size(CONS_G_M_time.val,1),1) = ["EXIOMOD 2.0" ];
CONS_G_M_time_OE(:,2)=stringtable(:,1);
CONS_G_M_time_OE(:,3)=stringtable(:,3);
CONS_G_M_time_OE(:,4)=strcat("Consumption|Government|",stringtable(:,2),"|Imported");
CONS_G_M_time_OE(:,5)="million euro/yr";
CONS_G_M_time_OE(:,6)=stringtable(:,4);
CONS_G_M_time_OE(:,7)=CONS_G_M_time.val(:,5);

CONS_G_M_time_OE_table = array2table(CONS_G_M_time_OE,...
    'VariableNames',{'Model','Scenario','Region','Variable','Unit','Year','Value'});

CONS_G_M_time_OE_table.Value=str2double(CONS_G_M_time_OE_table.Value);

CONS_G_M_time_OE_table_unstack = unstack(CONS_G_M_time_OE_table,'Value','Year');

%% CONS_G_D_time
"CONS_G_D_time"

clear stringtable
tic
for j=1:size(CONS_G_D_time.val,2)-1
    for i=1:size(CONS_G_D_time.val,1)
        set_idx=CONS_G_D_time.val(i,j);
        stringtable(i,j)=string(CONS_G_D_time.uels{1,1}{1,set_idx}); 
    end
end
toc

CONS_G_D_time_OE(1:size(CONS_G_D_time.val,1),1) = ["EXIOMOD 2.0" ];
CONS_G_D_time_OE(:,2)=stringtable(:,1);
CONS_G_D_time_OE(:,3)=stringtable(:,3);
CONS_G_D_time_OE(:,4)=strcat("Consumption|Government|",stringtable(:,2),"|Domestic");
CONS_G_D_time_OE(:,5)="million euro/yr";
CONS_G_D_time_OE(:,6)=stringtable(:,4);
CONS_G_D_time_OE(:,7)=CONS_G_D_time.val(:,5);

CONS_G_D_time_OE_table = array2table(CONS_G_D_time_OE,...
    'VariableNames',{'Model','Scenario','Region','Variable','Unit','Year','Value'});

CONS_G_D_time_OE_table.Value=str2double(CONS_G_D_time_OE_table.Value);

CONS_G_D_time_OE_table_unstack = unstack(CONS_G_D_time_OE_table,'Value','Year');

%% GFCF_M_time
"GFCF_M_time"

clear stringtable
tic
for j=1:size(GFCF_M_time.val,2)-1
    for i=1:size(GFCF_M_time.val,1)
        set_idx=GFCF_M_time.val(i,j);
        stringtable(i,j)=string(GFCF_M_time.uels{1,1}{1,set_idx}); 
    end
end
toc

GFCF_M_time_OE(1:size(GFCF_M_time.val,1),1) = ["EXIOMOD 2.0" ];
GFCF_M_time_OE(:,2)=stringtable(:,1);
GFCF_M_time_OE(:,3)=stringtable(:,3);
GFCF_M_time_OE(:,4)=strcat("Gross Capital Formation|",stringtable(:,2),"|Imported");
GFCF_M_time_OE(:,5)="million euro/yr";
GFCF_M_time_OE(:,6)=stringtable(:,4);
GFCF_M_time_OE(:,7)=GFCF_M_time.val(:,5);

GFCF_M_time_OE_table = array2table(GFCF_M_time_OE,...
    'VariableNames',{'Model','Scenario','Region','Variable','Unit','Year','Value'});

GFCF_M_time_OE_table.Value=str2double(GFCF_M_time_OE_table.Value);

GFCF_M_time_OE_table_unstack = unstack(GFCF_M_time_OE_table,'Value','Year');

%% GFCF_D_time
"GFCF_D_time"

clear stringtable
tic
for j=1:size(GFCF_D_time.val,2)-1
    for i=1:size(GFCF_D_time.val,1)
        set_idx=GFCF_D_time.val(i,j);
        stringtable(i,j)=string(GFCF_D_time.uels{1,1}{1,set_idx}); 
    end
end
toc

GFCF_D_time_OE(1:size(GFCF_D_time.val,1),1) = ["EXIOMOD 2.0" ];
GFCF_D_time_OE(:,2)=stringtable(:,1);
GFCF_D_time_OE(:,3)=stringtable(:,3);
GFCF_D_time_OE(:,4)=strcat("Gross Capital Formation|",stringtable(:,2),"|Domestic");
GFCF_D_time_OE(:,5)="million euro/yr";
GFCF_D_time_OE(:,6)=stringtable(:,4);
GFCF_D_time_OE(:,7)=GFCF_D_time.val(:,5);

GFCF_D_time_OE_table = array2table(GFCF_D_time_OE,...
    'VariableNames',{'Model','Scenario','Region','Variable','Unit','Year','Value'});

GFCF_D_time_OE_table.Value=str2double(GFCF_D_time_OE_table.Value);

GFCF_D_time_OE_table_unstack = unstack(GFCF_D_time_OE_table,'Value','Year');


%% TOTCONS_time.name='TOTCONS_time' 
"TOTCONS_time"

clear stringtable
tic
for j=1:size(TOTCONS_time.val,2)-1
    for i=1:size(TOTCONS_time.val,1)
        set_idx=TOTCONS_time.val(i,j);
        stringtable(i,j)=string(TOTCONS_time.uels{1,1}{1,set_idx}); 
    end
end
toc

TOTCONS_time_OE(1:size(TOTCONS_time.val,1),1) = ["EXIOMOD 2.0" ];
TOTCONS_time_OE(:,2)=stringtable(:,1);
TOTCONS_time_OE(:,3)=stringtable(:,2);
TOTCONS_time_OE(:,4)=strcat("Consumption");
TOTCONS_time_OE(:,5)="million euro/yr";
TOTCONS_time_OE(:,6)=stringtable(:,3);
TOTCONS_time_OE(:,7)=TOTCONS_time.val(:,4);

TOTCONS_time_OE_table = array2table(TOTCONS_time_OE,...
    'VariableNames',{'Model','Scenario','Region','Variable','Unit','Year','Value'});

TOTCONS_time_OE_table.Value=str2double(TOTCONS_time_OE_table.Value);

TOTCONS_time_OE_table_unstack = unstack(TOTCONS_time_OE_table,'Value','Year');


%% CONS_H_TT_time.name='CONS_H_TT_time' 
"CONS_H_TT_time"

clear stringtable
tic
for j=1:size(CONS_H_TT_time.val,2)-1
    for i=1:size(CONS_H_TT_time.val,1)
        set_idx=CONS_H_TT_time.val(i,j);
        stringtable(i,j)=string(CONS_H_TT_time.uels{1,1}{1,set_idx}); 
    end
end
toc

CONS_H_TT_time_OE(1:size(CONS_H_TT_time.val,1),1) = ["EXIOMOD 2.0" ];
CONS_H_TT_time_OE(:,2)=stringtable(:,1);
CONS_H_TT_time_OE(:,3)=stringtable(:,2);
CONS_H_TT_time_OE(:,4)=strcat("Consumption|Households");
CONS_H_TT_time_OE(:,5)="million euro/yr";
CONS_H_TT_time_OE(:,6)=stringtable(:,3);
CONS_H_TT_time_OE(:,7)=CONS_H_TT_time.val(:,4);

CONS_H_TT_time_OE_table = array2table(CONS_H_TT_time_OE,...
    'VariableNames',{'Model','Scenario','Region','Variable','Unit','Year','Value'});

CONS_H_TT_time_OE_table.Value=str2double(CONS_H_TT_time_OE_table.Value);

CONS_H_TT_time_OE_table_unstack = unstack(CONS_H_TT_time_OE_table,'Value','Year');

%% CONS_G_TT_time.name='CONS_G_TT_time' 
"CONS_G_TT_time"

clear stringtable
tic
for j=1:size(CONS_G_TT_time.val,2)-1
    for i=1:size(CONS_G_TT_time.val,1)
        set_idx=CONS_G_TT_time.val(i,j);
        stringtable(i,j)=string(CONS_G_TT_time.uels{1,1}{1,set_idx}); 
    end
end
toc

CONS_G_TT_time_OE(1:size(CONS_G_TT_time.val,1),1) = ["EXIOMOD 2.0" ];
CONS_G_TT_time_OE(:,2)=stringtable(:,1);
CONS_G_TT_time_OE(:,3)=stringtable(:,2);
CONS_G_TT_time_OE(:,4)=strcat("Consumption|Government");
CONS_G_TT_time_OE(:,5)="million euro/yr";
CONS_G_TT_time_OE(:,6)=stringtable(:,3);
CONS_G_TT_time_OE(:,7)=CONS_G_TT_time.val(:,4);

CONS_G_TT_time_OE_table = array2table(CONS_G_TT_time_OE,...
    'VariableNames',{'Model','Scenario','Region','Variable','Unit','Year','Value'});

CONS_G_TT_time_OE_table.Value=str2double(CONS_G_TT_time_OE_table.Value);

CONS_G_TT_time_OE_table_unstack = unstack(CONS_G_TT_time_OE_table,'Value','Year');


%% INTER_USE_TT_time.name='INTER_USE_TT_time' 
"INTER_USE_TT_time"

clear stringtable
tic
for j=1:size(INTER_USE_TT_time.val,2)-1
    for i=1:size(INTER_USE_TT_time.val,1)
        set_idx=INTER_USE_TT_time.val(i,j);
        stringtable(i,j)=string(INTER_USE_TT_time.uels{1,1}{1,set_idx}); 
    end
end
toc

INTER_USE_TT_time_OE(1:size(INTER_USE_TT_time.val,1),1) = ["EXIOMOD 2.0" ];
INTER_USE_TT_time_OE(:,2)=stringtable(:,1);
INTER_USE_TT_time_OE(:,3)=stringtable(:,2);
INTER_USE_TT_time_OE(:,4)=strcat("Consumption|Industry");
INTER_USE_TT_time_OE(:,5)="million euro/yr";
INTER_USE_TT_time_OE(:,6)=stringtable(:,3);
INTER_USE_TT_time_OE(:,7)=INTER_USE_TT_time.val(:,4);

INTER_USE_TT_time_OE_table = array2table(INTER_USE_TT_time_OE,...
    'VariableNames',{'Model','Scenario','Region','Variable','Unit','Year','Value'});

INTER_USE_TT_time_OE_table.Value=str2double(INTER_USE_TT_time_OE_table.Value);

INTER_USE_TT_time_OE_table_unstack = unstack(INTER_USE_TT_time_OE_table,'Value','Year');


%% INTER_USE_MM_time.name='INTER_USE_MM_time' 
"INTER_USE_MM_time"

clear stringtable
tic
for j=1:size(INTER_USE_MM_time.val,2)-1
    for i=1:size(INTER_USE_MM_time.val,1)
        set_idx=INTER_USE_MM_time.val(i,j);
        stringtable(i,j)=string(INTER_USE_MM_time.uels{1,1}{1,set_idx}); 
    end
end
toc

INTER_USE_MM_time_OE(1:size(INTER_USE_MM_time.val,1),1) = ["EXIOMOD 2.0" ];
INTER_USE_MM_time_OE(:,2)=stringtable(:,1);
INTER_USE_MM_time_OE(:,3)=stringtable(:,3);
INTER_USE_MM_time_OE(:,4)=strcat("Consumption|Industry|",stringtable(:,2),"|Import");
INTER_USE_MM_time_OE(:,5)="million euro/yr";
INTER_USE_MM_time_OE(:,6)=stringtable(:,4);
INTER_USE_MM_time_OE(:,7)=INTER_USE_MM_time.val(:,5);

INTER_USE_MM_time_OE_table = array2table(INTER_USE_MM_time_OE,...
    'VariableNames',{'Model','Scenario','Region','Variable','Unit','Year','Value'});

INTER_USE_MM_time_OE_table.Value=str2double(INTER_USE_MM_time_OE_table.Value);

INTER_USE_MM_time_OE_table_unstack = unstack(INTER_USE_MM_time_OE_table,'Value','Year');

%% INTER_USE_DD_time.name='INTER_USE_DD_time' 
"INTER_USE_DD_time"

clear stringtable
tic
for j=1:size(INTER_USE_DD_time.val,2)-1
    for i=1:size(INTER_USE_DD_time.val,1)
        set_idx=INTER_USE_DD_time.val(i,j);
        stringtable(i,j)=string(INTER_USE_DD_time.uels{1,1}{1,set_idx}); 
    end
end
toc

INTER_USE_DD_time_OE(1:size(INTER_USE_DD_time.val,1),1) = ["EXIOMOD 2.0" ];
INTER_USE_DD_time_OE(:,2)=stringtable(:,1);
INTER_USE_DD_time_OE(:,3)=stringtable(:,3);
INTER_USE_DD_time_OE(:,4)=strcat("Consumption|Industry|",stringtable(:,2),"|Domestic");
INTER_USE_DD_time_OE(:,5)="million euro/yr";
INTER_USE_DD_time_OE(:,6)=stringtable(:,4);
INTER_USE_DD_time_OE(:,7)=INTER_USE_DD_time.val(:,5);

INTER_USE_DD_time_OE_table = array2table(INTER_USE_DD_time_OE,...
    'VariableNames',{'Model','Scenario','Region','Variable','Unit','Year','Value'});

INTER_USE_DD_time_OE_table.Value=str2double(INTER_USE_DD_time_OE_table.Value);

INTER_USE_DD_time_OE_table_unstack = unstack(INTER_USE_DD_time_OE_table,'Value','Year');

%% Place all tables together


OE_table = ...
vertcat(P_time_OE_table_unstack,...
        X_time_OE_table_unstack,...
        Y_time_OE_table_unstack,...
        GDPCONST_time_OE_table_unstack,...
        K_time_OE_table_unstack,...
        L_time_OE_table_unstack,...
        PK_time_OE_table_unstack,...
        PL_time_OE_table_unstack,...
        CONS_G_D_time_OE_table_unstack,...
        CONS_G_M_time_OE_table_unstack,...
        CONS_H_D_time_OE_table_unstack,...
        CONS_H_M_time_OE_table_unstack,...
        GFCF_D_time_OE_table_unstack,...
        GFCF_M_time_OE_table_unstack,...
        TOTCONS_time_OE_table_unstack,... 
        CONS_H_TT_time_OE_table_unstack,... 
        CONS_G_TT_time_OE_table_unstack,... 
        INTER_USE_TT_time_OE_table_unstack,... 
        INTER_USE_MM_time_OE_table_unstack,... 
        INTER_USE_DD_time_OE_table_unstack ); 
 
%% Make connection to regions as defined by Platform

Country_def=["AUT" "Austria";...
"BEL" "Belgium";...
"BGR" "Bulgaria";...
"HRV" "Croatia";...
"CZE" "Czech Republic";...
"CYP" "Cyprus";...
"DNK" "Denmark";...
"EST" "Estonia";...
"FIN" "Finland";...
"FRA" "France";...
"GRC" "Greece";...
"HUN" "Hungary";...
"ITA" "Italy";...
"LVA" "Latvia";...
"LTU" "Lithuania";...
"LUX" "Luxembourg";...
"MLT" "Malta";...
"NLD" "The Netherlands";...
"POL" "Poland";...
"PRT" "Portugal";...
"ROU" "Romania";...
"SVK" "Slovakia";...
"SVN" "Slovenia";...
"ESP" "Spain";...
"SWE" "Sweden";...
"GBR" "United Kingdom";...
%"RWO" "Rest of World O";...
%"RWN" "Rest of World N";...
"DEU" "Germany";...
"IRL" "Ireland"];


   xxx=find(ismember(OE_table.Region,"RWO"));
   OE_table(xxx,:)=[]; 
   xxx=find(ismember(OE_table.Region,"RWN"));
   OE_table(xxx,:)=[];
   
for i=1:size(Country_def,1)
   xxx=find(ismember(OE_table.Region,Country_def(i,1)));
   OE_table.Region(xxx)=Country_def(i,2); 
end
    

    
%% Write data to excel
% writetable(P_time_OE_table_unstack,'project_open_entrance\03_simulation_results\Output\Result_matlab.xlsx','Sheet','P_time')
% writetable(X_time_OE_table_unstack,'project_open_entrance\03_simulation_results\Output\Result_matlab.xlsx','Sheet','X_time')
% writetable(Y_time_OE_table_unstack,'project_open_entrance\03_simulation_results\Output\Result_matlab.xlsx','Sheet','Y_time')
% writetable(GDPCONST_time_OE_table_unstack,'project_open_entrance\03_simulation_results\Output\Result_matlab.xlsx','Sheet','GDPCONST_time')
% 
% writetable(K_time_OE_table_unstack,'project_open_entrance\03_simulation_results\Output\Result_matlab.xlsx','Sheet','K_time')
% writetable(L_time_OE_table_unstack,'project_open_entrance\03_simulation_results\Output\Result_matlab.xlsx','Sheet','L_time')
% writetable(PK_time_OE_table_unstack,'project_open_entrance\03_simulation_results\Output\Result_matlab.xlsx','Sheet','PK_time')
% writetable(PL_time_OE_table_unstack,'project_open_entrance\03_simulation_results\Output\Result_matlab.xlsx','Sheet','PL_time')
% 
% writetable(CONS_G_D_time_OE_table_unstack,'project_open_entrance\03_simulation_results\Output\Result_matlab.xlsx','Sheet','CONS_G_D_time')
% writetable(CONS_G_M_time_OE_table_unstack,'project_open_entrance\03_simulation_results\Output\Result_matlab.xlsx','Sheet','CONS_G_M_time')
% writetable(CONS_H_D_time_OE_table_unstack,'project_open_entrance\03_simulation_results\Output\Result_matlab.xlsx','Sheet','CONS_H_D_time')
% writetable(CONS_H_M_time_OE_table_unstack,'project_open_entrance\03_simulation_results\Output\Result_matlab.xlsx','Sheet','CONS_H_M_time')
% writetable(GFCF_D_time_OE_table_unstack,'project_open_entrance\03_simulation_results\Output\Result_matlab.xlsx','Sheet','GFCF_D_time')
% writetable(GFCF_M_time_OE_table_unstack,'project_open_entrance\03_simulation_results\Output\Result_matlab.xlsx','Sheet','GFCF_M_time')

writetable(OE_table,'project_open_entrance\03_simulation_results\Output\Result_matlab.xlsx','Sheet','data')

