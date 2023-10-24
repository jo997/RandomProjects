using System;
using System.Collections.Generic;
using System.Threading;

public class Node
{
    public int X { get; }
    public int Y { get; }
    public bool IsObstacle { get; set; }
    public bool IsVisited { get; set; }

    public Node(int x, int y)
    {
        X = x;
        Y = y;
        IsObstacle = false;
        IsVisited = false;
    }
}

public class Grid
{
    public int Width { get; }
    public int Height { get; }
    public Node[,] Nodes { get; }
    public Node Start { get; private set; }
    public Node End { get; private set; }

    public Grid(int width, int height)
    {
        Width = width;
        Height = height;
        Nodes = new Node[width, height];
        InitializeNodes();
    }

    private void InitializeNodes()
    {
        for (int i = 0; i < Width; i++)
        {
            for (int j = 0; j < Height; j++)
            {
                Nodes[i, j] = new Node(i, j);
            }
        }
    }

    public void SetStart(int x, int y)
    {
        Start = Nodes[x, y];
    }

    public void SetEnd(int x, int y)
    {
        End = Nodes[x, y];
    }

    public void SetObstacle(int x, int y)
    {
        Nodes[x, y].IsObstacle = true;
    }

    public void PrintGrid(Node currentNode)
    {
        Console.Clear();

        for (int i = -1; i <= Height; i++)
        {
            for (int j = -1; j <= Width; j++)
            {
                if (i == -1 || i == Height || j == -1 || j == Width)
                {
                    Console.Write("# "); // Border
                }
                else
                {
                    Node node = Nodes[j, i];
                    if (node == Start)
                        Console.Write("S ");
                    else if (node == End)
                        Console.Write("G ");
                    else if (node.IsObstacle)
                        Console.Write("X ");
                    else if (node.IsVisited)
                        Console.Write("=");
                    else if (node == currentNode)
                        Console.Write("O "); // Current node on path
                    else
                        Console.Write("  ");
                }
            }
            Console.WriteLine();
        }
        Console.WriteLine();
    }

    public void FollowPath(List<Node> path)
    {
        foreach (var node in path)
        {
            PrintGrid(node);
            Thread.Sleep(50); // Add a delay for visibility
        }
    }
}

public class PathfindingSimulation
{
    static Random random = new Random();

    static List<Node> GetNeighbors(Node[,] nodes, Node node)
    {
        List<Node> neighbors = new List<Node>();

        int[] dx = { -1, 1, 0, 0 };
        int[] dy = { 0, 0, -1, 1 };

        for (int i = 0; i < 4; i++)
        {
            int nx = node.X + dx[i];
            int ny = node.Y + dy[i];

            if (nx >= 0 && nx < nodes.GetLength(0) && ny >= 0 && ny < nodes.GetLength(1))
            {
                neighbors.Add(nodes[nx, ny]);
            }
        }

        return neighbors;
    }

static List<Node> AStar(Grid grid)
{
    List<Node> path = new List<Node>();

    HashSet<Node> openSet = new HashSet<Node>();
    HashSet<Node> closedSet = new HashSet<Node>();

    Dictionary<Node, Node> cameFrom = new Dictionary<Node, Node>();

    Dictionary<Node, int> gScore = new Dictionary<Node, int>();
    Dictionary<Node, int> fScore = new Dictionary<Node, int>();

    foreach (var node in grid.Nodes)
    {
        gScore[node] = int.MaxValue;
        fScore[node] = int.MaxValue;
    }

    gScore[grid.Start] = 0;
    fScore[grid.Start] = Heuristic(grid.Start, grid.End);

    openSet.Add(grid.Start);

    while (openSet.Count > 0)
    {
        Node current = null;

        foreach (var node in openSet)
        {
            if (current == null || fScore[node] < fScore[current])
            {
                current = node;
            }
        }

        if (current == grid.End)
        {
            while (cameFrom.ContainsKey(current))
            {
                path.Add(current);
                current = cameFrom[current];
            }

            break;
        }

        openSet.Remove(current);
        closedSet.Add(current);

        foreach (var neighbor in GetNeighbors(grid.Nodes, current))
        {
            if (neighbor.IsObstacle || closedSet.Contains(neighbor))
                continue;

            int tentativeGScore = gScore[current] + 1; // Assuming uniform edge weights of 1

            if (!openSet.Contains(neighbor))
                openSet.Add(neighbor);
            else if (tentativeGScore >= gScore[neighbor])
                continue;

            cameFrom[neighbor] = current;
            gScore[neighbor] = tentativeGScore;
            fScore[neighbor] = gScore[neighbor] + Heuristic(neighbor, grid.End);
        }
    }

    path.Reverse();
    return path;
}

static int Heuristic(Node a, Node b)
{
    // This is a simple Manhattan distance heuristic, you can use other heuristics as well.
    return Math.Abs(a.X - b.X) + Math.Abs(a.Y - b.Y);
}

   static List<Node> Dijkstra(Grid grid)
{
    List<Node> path = new List<Node>();

    Dictionary<Node, int> distance = new Dictionary<Node, int>();
    Dictionary<Node, Node> previous = new Dictionary<Node, Node>();
    HashSet<Node> unvisited = new HashSet<Node>();

    foreach (var node in grid.Nodes)
    {
        distance[node] = int.MaxValue;
        previous[node] = null;
        unvisited.Add(node);
    }

    distance[grid.Start] = 0;

    while (unvisited.Count > 0)
    {
        Node current = null;

        foreach (var node in unvisited)
        {
            if (current == null || distance[node] < distance[current])
            {
                current = node;
            }
        }

        unvisited.Remove(current);

        if (current == grid.End)
        {
            while (previous[current] != null)
            {
                path.Add(current);
                current = previous[current];
            }

            break;
        }

        foreach (var neighbor in GetNeighbors(grid.Nodes, current))
        {
            if (!neighbor.IsObstacle) // Check if neighbor is an obstacle
            {
                int alt = distance[current] + 1; // Assuming uniform edge weights of 1

                if (alt < distance[neighbor])
                {
                    distance[neighbor] = alt;
                    previous[neighbor] = current;
                }
            }
        }
    }

    path.Reverse();
    return path;
}

public static void AddObstacleRectangle(Grid grid, int startX, int startY, int endX, int endY)
{
    for (int i = startX; i <= endX; i++)
    {
        for (int j = startY; j <= endY; j++)
        {
            grid.SetObstacle(i, j);
        }
    }
}

public static void Maze1(Grid grid)
{
    grid.SetStart(1, 1);
    grid.SetEnd(18, 18);

    AddObstacleRectangle(grid, 0, 0, 19, 1);
    AddObstacleRectangle(grid, 0, 0, 1, 19);
    AddObstacleRectangle(grid, 0, 18, 19, 19);
    AddObstacleRectangle(grid, 18, 0, 19, 18);

    for (int i = 3; i <= 16; i += 2)
    {
        grid.SetObstacle(i, 8);
    }
}



public static void Maze2(Grid grid)
{
    grid.SetStart(1, 1);
    grid.SetEnd(13, 13);

    AddObstacleRectangle(grid, 1, 1, 13, 1);
    AddObstacleRectangle(grid, 1, 1, 1, 13);
    AddObstacleRectangle(grid, 1, 13, 13, 13);
    AddObstacleRectangle(grid, 13, 1, 13, 12);
    AddObstacleRectangle(grid, 3, 3, 11, 3);
    AddObstacleRectangle(grid, 3, 5, 3, 11);
    AddObstacleRectangle(grid, 3, 5, 9, 5);
    AddObstacleRectangle(grid, 9, 5, 9, 9);
    AddObstacleRectangle(grid, 5, 9, 9, 9);
    AddObstacleRectangle(grid, 5, 7, 7, 7);
    AddObstacleRectangle(grid, 5, 7, 7, 7);

    grid.Nodes[1, 1].IsObstacle = false;
    grid.Nodes[13, 13].IsObstacle = false;
}

public static void Maze3(Grid grid)
{
    grid.SetStart(1, 1);
    grid.SetEnd(13, 13);

    AddObstacleRectangle(grid, 1, 1, 13, 1);
    AddObstacleRectangle(grid, 1, 1, 1, 13);
    AddObstacleRectangle(grid, 1, 13, 13, 13);
    AddObstacleRectangle(grid, 13, 1, 13, 12);
    AddObstacleRectangle(grid, 3, 3, 11, 3);
    AddObstacleRectangle(grid, 3, 5, 3, 11);
    AddObstacleRectangle(grid, 3, 5, 9, 5);
    AddObstacleRectangle(grid, 9, 5, 9, 9);
    AddObstacleRectangle(grid, 5, 9, 9, 9);
    AddObstacleRectangle(grid, 5, 7, 7, 7);

    grid.Nodes[1, 1].IsObstacle = false;
    grid.Nodes[13, 13].IsObstacle = false;

    AddObstacleRectangle(grid, 5, 4, 8, 4);
    AddObstacleRectangle(grid, 5, 10, 8, 10);
}

public static void Maze4(Grid grid)
{
    grid.SetStart(1, 1);
    grid.SetEnd(13, 13);

    AddObstacleRectangle(grid, 1, 1, 13, 1);
    AddObstacleRectangle(grid, 1, 1, 1, 13);
    AddObstacleRectangle(grid, 1, 13, 13, 13);
    AddObstacleRectangle(grid, 13, 1, 13, 12);
    AddObstacleRectangle(grid, 3, 3, 11, 3);
    AddObstacleRectangle(grid, 3, 5, 3, 11);
    AddObstacleRectangle(grid, 3, 5, 9, 5);
    AddObstacleRectangle(grid, 9, 5, 9, 9);
    AddObstacleRectangle(grid, 5, 9, 9, 9);
    AddObstacleRectangle(grid, 5, 7, 7, 7);

    grid.Nodes[1, 1].IsObstacle = false;
    grid.Nodes[13, 13].IsObstacle = false;

    AddObstacleRectangle(grid, 5, 4, 8, 4);
    AddObstacleRectangle(grid, 5, 10, 8, 10);
    AddObstacleRectangle(grid, 5, 6, 8, 6);
}




static void Main()
    {
        
        Grid grid = new Grid(20, 20);
        Maze1(grid); // Use Maze1
        // OR
        //Maze2(grid); // Use Maze2
        // OR
        //Maze3(grid); // Use Maze3
        // OR
        //Maze4(grid); // Use Maze4

        grid.PrintGrid(null);

        //List<Node> path = Dijkstra(grid);
        List<Node> path = AStar(grid);

        grid.FollowPath(path);

        Console.WriteLine("Path found!");
    }
}
