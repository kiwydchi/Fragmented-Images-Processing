function [TR,TT,data] = icp(model,data,maxIter,minIter,critFun,thres)
if nargin<2
    
    error('To few input arguments');
    
elseif nargin<6
    
    thres=1e-5;                     % порог остановки
    if nargin<5
        critFun=0;                  % выбор функции
        if nargin<4
            minIter=5;              % мин. кол-во итераций
            if nargin<3
                maxIter=100;        % max number of icp iterations
            end
        end
    end
    
end
if or(isempty(model),isempty(data))
    error('Ошибка в модели данных');
end
% Задание стандартных значений
if isempty(maxIter)
    maxIter=100;
end
if isempty(minIter)
    minIter=5;
end
if isempty(critFun)
    critFun=0;
end
if isempty(thres)
    thres=1e-5;
end
% Определение размерностей
if (size(model,2)<size(model,1))
    mTranspose=true;
    m=size(model,2);
    M=size(model,1);
else
    mTranspose=false;
    m=size(model,1);
    M=size(model,2);
end
if (size(data,2)<size(data,1))
    data=data';
end
if m~=size(data,1)
    error('Размерности не одинаковы');
end
N=size(data,2);
% Составление структуры поиска двух ближайших точек
if m<4
    if mTranspose
        DT=delaunayTriangulation(model);
    else
        DT=delaunayTriangulation(model');
    end
else
    DT=[];
    resid=zeros(N,1);
    vi=ones(N,1);
end
% Инициализация трансформации
TR=eye(m);
TT=zeros(m,1);
% Начало алгоритма
res=9e99;
for iter=1:maxIter
    
    oldres=res;
    
    % Поиск ближайих точек из двух облаков
    
    if isempty(DT)
        if mTranspose
            for i=1:N
                mival=9e99;
                for j=1:M
                    val=norm(data(:,i)-model(j,:)');
                    if val<mival
                        mival=val;
                        vi(i)=j;
                        resid(i)=val;
                    end
                end
            end
        else
            for i=1:N
                mival=9e99;
                for j=1:M
                    val=norm(data(:,i)-model(:,j));
                    if val<mival
                        mival=val;
                        vi(i)=j;
                        resid(i)=val;
                    end
                end
            end
        end
    else
        [vi,resid] = nearestNeighbor(DT,data');
    end
    
    switch critFun
        
        case 0
            
            res=mean(resid.^2);
            
            med=mean(data,2);
            if mTranspose
                mem=mean(model(vi,:),1);
                C=data*model(vi,:)-(N*med)*mem;
                [U,~,V]=svd(C);
                Ri=V*U';
                if det(Ri)<0
                    V(:,end)=-V(:,end);
                    Ri=V*U';
                end
                Ti=mem'-Ri*med;
            else
                mem=mean(model(:,vi),2);
                C=data*model(:,vi)'-(N*med)*mem';
                [U,~,V]=svd(C);
                Ri=V*U';
                if det(Ri)<0
                    V(:,end)=-V(:,end);
                    Ri=V*U';
                end
                Ti=mem-Ri*med;
            end
            
        otherwise
            
            kRob = 1.9*median(resid);
            
            maxResid=max(resid);
            if kRob<1e-6*maxResid
                kRob=0.3*maxResid;
            elseif maxResid==0
                kRob=1;
            end
            
            res=mean(resid(resid<1.5*kRob).^2);
            suWghs=sum(wghs);
            
            med=(data*wghs)/suWghs;
            if mTranspose
                mem=(wghs'*model(vi,:))/suWghs;
                C=data*(model(vi,:).*repmat(wghs,1,m))-(suWghs*med)*mem;
                [U,~,V]=svd(C);
                Ri=V*U';
                if det(Ri)<0
                    V(:,end)=-V(:,end);
                    Ri=V*U';
                end
                Ti=mem'-Ri*med;
            else
                mem=(model(:,vi)*wghs)/suWghs;
                C=(data.*repmat(wghs',m,1))*model(:,vi)'-(suWghs*med)*mem';
                [U,~,V]=svd(C);
                Ri=V*U';
                if det(Ri)<0
                    V(:,end)=-V(:,end);
                    Ri=V*U';
                end
                Ti=mem-Ri*med;
            end
            
    end
    
    data=Ri*data;                       % Применение трансформации
    for i=1:m
        data(i,:)=data(i,:)+Ti(i);
    end
    
    TR=Ri*TR;
    TT=Ri*TT+Ti;
    
    if iter >= minIter
        if abs(oldres-res) < thres
            break
        end
    end
    
end
