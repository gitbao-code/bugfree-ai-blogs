---
title: "Designing a Chess Game: The Roblox New Grad Interview"
datePublished: Wed Feb 12 2025 17:42:20 GMT+0000 (Coordinated Universal Time)
cuid: cm8vzxeps000409l269n65dv8
slug: designing-a-chess-game-the-roblox-new-grad-interview-20637508b994
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1743360664172/0f810dce-3e26-4a21-b156-fddef39cf8d9.png

---

Designing a Chess Game is a frequently asked object oriented design even for new grads.

In this post, we explore the key aspects of designing a chess game with an object-oriented approach, focusing on core object modeling, encapsulation, polymorphism, design patterns, object relationships, scalability, and technical considerations, together with code snippets.

System Design Diagram — Design Chess Game

### 1\. Core Object Modeling

#### ChessBoard

The `ChessBoard` class manages the state of the game and provides methods for piece placement and movement tracking. Key considerations include:

*   **Data Structure for Board Representation**: Should we use a 2D array (8x8 matrix), a hashmap, or a graph-based approach? A 2D array is straightforward, while a hashmap can optimize lookup times for sparse board representations.
*   **Encapsulation of Board State**: The board should provide an interface to query and modify positions without exposing the internal representation.
*   **Move History Storage**: The board should maintain a history of moves for undo functionality and replay features.

class ChessBoard {  
    private Piece\[\]\[\] board;  
    private List<Move> moveHistory;  
      
    public ChessBoard() {  
        this.board = new Piece\[8\]\[8\];  
        this.moveHistory = new ArrayList<>();  
        initializeBoard();  
    }  
      
    private void initializeBoard() {  
        // Place pieces in initial positions using PieceFactory  
    }  
      
    public void movePiece(Position from, Position to) {  
        moveHistory.add(new Move(from, to, board\[to.getX()\]\[to.getY()\]));  
        board\[to.getX()\]\[to.getY()\] = board\[from.getX()\]\[from.getY()\];  
        board\[from.getX()\]\[from.getY()\] = null;  
    }  
}

#### Piece and Its Variants

*   The `Piece` class is an abstract class representing a chess piece.
*   Each piece type (Pawn, Rook, Knight, Bishop, Queen, King) extends this class and implements movement rules.
*   **Encapsulation**: Each piece controls its own move logic through polymorphism.

abstract class Piece {  
    protected Position position;  
    protected boolean isWhite;  
      
    public Piece(Position position, boolean isWhite) {  
        this.position = position;  
        this.isWhite = isWhite;  
    }  
      
    public abstract boolean isValidMove(Position newPosition, ChessBoard board);  
}

### 2\. Design Patterns in Chess Game Design

#### a) Factory Pattern

Used for creating chess pieces dynamically based on type.

class PieceFactory {  
    public static Piece createPiece(String type, boolean isWhite) {  
        switch (type) {  
            case "Pawn": return new Pawn(isWhite);  
            case "Knight": return new Knight(isWhite);  
            case "Bishop": return new Bishop(isWhite);  
            case "Rook": return new Rook(isWhite);  
            case "Queen": return new Queen(isWhite);  
            case "King": return new King(isWhite);  
            default: throw new IllegalArgumentException("Invalid piece type");  
        }  
    }  
}

#### b) Strategy Pattern

Encapsulates different move validation strategies for each piece.

interface MoveStrategy {  
    boolean isValidMove(Position from, Position to, ChessBoard board);  
}

class BishopMoveStrategy implements MoveStrategy {  
    public boolean isValidMove(Position from, Position to, ChessBoard board) {  
        return Math.abs(from.getX() - to.getX()) == Math.abs(from.getY() - to.getY());  
    }  
}

Each piece class uses a different move strategy:

class Bishop extends Piece {  
    public Bishop(boolean isWhite) {  
        super(isWhite, new BishopMoveStrategy());  
    }  
}

#### c) Observer Pattern

Used for notifying the UI or players about game state changes.

interface GameObserver {  
    void onMoveMade(Move move);  
}  
  
class ChessGameUI implements GameObserver {  
    public void onMoveMade(Move move) {  
        System.out.println("Move made: " + move);  
    }  
}

#### d) Command Pattern

Used for implementing undo/redo functionality.

interface Command {  
    void execute();  
    void undo();  
}  
  
class MoveCommand implements Command {  
    private ChessBoard board;  
    private Position from, to;  
    private Piece capturedPiece;  
    public MoveCommand(ChessBoard board, Position from, Position to) {  
        this.board = board;  
        this.from = from;  
        this.to = to;  
    }  
    public void execute() {  
        capturedPiece = board.getPiece(to);  
        board.movePiece(from, to);  
    }  
    public void undo() {  
        board.movePiece(to, from);  
        board.placePiece(to, capturedPiece);  
    }  
}

#### e) Singleton Pattern

Ensures only one instance of `GameManager` exists at a time.

class GameManager {  
    private static GameManager instance;  
      
    private GameManager() {}  
      
    public static GameManager getInstance() {  
        if (instance == null) {  
            instance = new GameManager();  
        }  
        return instance;  
    }  
}

### 3\. Scalability Considerations

#### Database Choice and Storage Strategies

*   **Relational Database (PostgreSQL, MySQL)**: Suitable for structured data like player profiles, match history, and ELO ratings.
*   **NoSQL (MongoDB, DynamoDB)**: Useful for storing real-time game states and move history in a flexible JSON format.
*   **Redis**: Acts as an in-memory cache to store active game sessions, reducing database load and improving response times.
*   **Sharding and Replication**: For high scalability, distribute game sessions across multiple database instances and replicate read-heavy data.

#### Schema Design

Relational Database Schema (PostgreSQL/MySQL)

CREATE TABLE players (  
    id SERIAL PRIMARY KEY,  
    username VARCHAR(255) UNIQUE NOT NULL,  
    elo\_rating INT NOT NULL  
);  
  
CREATE TABLE games (  
    id SERIAL PRIMARY KEY,  
    white\_player\_id INT REFERENCES players(id),  
    black\_player\_id INT REFERENCES players(id),  
    status VARCHAR(50) CHECK (status IN ('ongoing', 'completed', 'abandoned')),  
    start\_time TIMESTAMP DEFAULT NOW(),  
    end\_time TIMESTAMP  
);  
  
CREATE TABLE moves (  
    id SERIAL PRIMARY KEY,  
    game\_id INT REFERENCES games(id),  
    move\_number INT NOT NULL,  
    piece VARCHAR(50) NOT NULL,  
    from\_position VARCHAR(5) NOT NULL,  
    to\_position VARCHAR(5) NOT NULL,  
    timestamp TIMESTAMP DEFAULT NOW()  
);

NoSQL Schema (MongoDB)

{  
    "game\_id": "12345",  
    "players": {  
        "white": "user1",  
        "black": "user2"  
    },  
    "moves": \[  
        { "move\_number": 1, "piece": "Pawn", "from": "e2", "to": "e4" },  
        { "move\_number": 2, "piece": "Knight", "from": "g8", "to": "f6" }  
    \],  
    "status": "ongoing",  
    "start\_time": "2023-07-01T12:00:00Z"  
}

### 4\. Handling Large Numbers of Games

*   **Game State Management**: Active games are stored in Redis for quick access, while completed games are persisted in a relational or NoSQL database.
*   **Session Management**: Each game instance is assigned a unique session ID, allowing efficient retrieval.
*   **Event Sourcing**: Instead of storing only the final board state, maintain a log of all moves to enable replay and rollback functionalities.

### 5\. Performance Optimization

*   **Bitboards** (64-bit integers) can be used for fast move computations by representing the board as a set of bitmaps.
*   **Precomputed attack tables** can optimize check and checkmate detection.
*   **Parallel Processing**: AI computations, such as Minimax and Alpha-Beta pruning, can be offloaded to separate threads or a distributed computing environment.
*   **Load Balancing**: Distribute game requests across multiple application instances using a load balancer.

### 6\. AI and Multiplayer Scalability

*   **AI Algorithms**: Minimax with Alpha-Beta pruning, Monte Carlo Tree Search (MCTS), or neural network-based approaches like AlphaZero.
*   **Multiplayer Game State Synchronization**: WebSockets for real-time move updates, ensuring seamless synchronization across clients.
*   **Conflict Resolution in Concurrent Games**: Implement atomic operations and locks to prevent simultaneous conflicting moves.

### 7\. Rule Variants Support

*   **Chess960** (randomized starting positions) can be implemented by modifying the board initialization logic.
*   **Custom game modes** with different board sizes or rules can be handled by modifying the piece factory and move strategies.

### 8\. Spectator Mode and Game History

*   Allow users to watch ongoing games with real-time updates.
*   Store move history in PGN (Portable Game Notation) format for replay analysis.
*   Implement a replay system that allows step-through navigation of past games.

Full Answer: [https://bugfree.ai/practice/object-oriented-design/chess-game/solutions/oYmdfuB0ooqAuX1d](https://bugfree.ai/practice/object-oriented-design/chess-game/solutions/oYmdfuB0ooqAuX1d)

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1743360660942/7891f7df-7602-470f-98bb-64fa122e49c6.png)

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1743360662664/48feaea8-3853-4a8a-8e4e-416b6bc044d1.png)

System Design Solution — Design Chess Game