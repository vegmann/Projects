%reads image
img = imread(['angel' ...
    '.jpg']);
gray = rgb2gray(img);
A = double(gray);

%svd
[U,S,V] = svd(A);
d=diag(S);
d_sorted = sort(d, 'ascend');
S_new = diag(d_sorted);
V=V';
a=150; %lower lim
b=467; %upper lim

%removes all singular values not within limits
A=U(:,a:b)*S_new(a:b,a:b)*V(a:b,:);

imshow(A,[0 255]);

