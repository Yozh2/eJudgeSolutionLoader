// This solution was sent via Python Script
#include <stdio.h>
typedef struct Point
{
        int x;
        int y;
} Point;
typedef struct Coord
{
        Point rb;
        Point lt;
} Coord;

int main ()
{
        int n, i, s;
        Coord a[1000];
        scanf ("%d", &n);
        s = 0;
        for (i = 0; i < n; i++)
        {
                scanf ("%d%d%d%d", &a[i].lt.x, &a[i].lt.y, &a[i].rb.x, &a[i].rb.y);
        }
        for (i = 0; i < n-1; i++)
        {
                if ((a[i].lt.x >= a[n-1].lt.x) && (a[i].lt.y <= a[n-1].lt.y) && (a[i].rb.x <= a[n-1].rb.x) && (a[i].rb.y >= a[n-1].rb.y))
                {
                        s++;
                }
        }
        printf ("%d\n", s);
        return 0;
}
