uses crt;
var
  n,m,i,j : longint;
  a : array[1..20,1..20] of longint;

function max(a,b:longint):longint;
begin
  if a>b
    then
      max:=a
    else
      max:=b;
end;

function f(x,y:longint):longint;
begin
  if (x=n) and (y=m)
    then
      f:=a[x,y]
    else
      if x=n
        then
          f:=f(x,y+1)+a[x,y]
        else
          if y=m
            then
              f:=f(x+1,y)+a[x,y]
            else
              f:=max(f(x+1,y),f(x,y+1))+a[x,y];
end;

begin
  readln(n,m);
  for i:=1 to n do
    begin
      for j:=1 to m do
        read(a[i,j]);
    end;
  writeln(f(1,1));
end.