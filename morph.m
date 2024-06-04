echo off
clear all;
close all;

fu8=imread('111.png');
[hg,wd,cn]=size(fu8);
figure; imshow(fu8);
f=mat2gray(fu8(:,:,1)); % ������� ���������� �����
A=im2bw(f); % �����������
figure; imshow(A);
A=imfill(A,'holes')~=A; % ���������� ������ ��� ��������� ���������
figure; imshow(A);
s=regionprops(A,'centroid'); % ��������� ������� ���������
centroids=round(cat(1,s.Centroid)); % ���������� �� �������
B=zeros(hg,wd); B(sub2ind(size(A),centroids(:,2),centroids(:,1)))=1;
figure; imshow(B);

%writematrix(centroids, 'coordstop.txt');% ������ ��������� ������� � ���� ��� ��������
centroids2=readmatrix("coordstop.txt");% ���������� ������ ��������� ��� ���������
model=rot90(centroids);%������������ ��������� � ������� ��� ���������� ����
data=rot90(centroids2);
i = 1;% ����� �������� ������ ��� ��������� ������
while i < height(centroids2)
    data(1,i) = data(1,i) + 10;
    data(2,i) = data(2,i) + 10;
    i = i + 1;
end
figure(1)
plot(model(1,:),model(2,:),'r.',data(1,:),data(2,:),'b.'), axis equal % ����� ��������� ������
[RotMat,TransVec,dataOut]=icp(model,data);%���������� ��������� ICP
figure(2)
plot(model(1,:),model(2,:),'r.',dataOut(1,:),dataOut(2,:),'b.'), axis equal % ����� ���������