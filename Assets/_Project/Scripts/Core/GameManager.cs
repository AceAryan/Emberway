using UnityEngine;

public enum GameState
{
    Boot,
    MainMenu,
    Playing,
    Paused,
    GameOver,
    GameCompleted
}

public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; }

    private GameState _currentState;
    public GameState CurrentState => _currentState;

    private void Awake()
    {
        // Singleton pattern - only one GameManager exists ever
        if (Instance != null && Instance != this)
        {
            Destroy(gameObject);
            return;
        }
        Instance = this;
        DontDestroyOnLoad(gameObject); // persists across scene loads
    }

    private void Start()
    {
        TransitionTo(GameState.Boot);
    }

    public void TransitionTo(GameState newState)
    {
        OnExit(_currentState);
        _currentState = newState;
        OnEnter(newState);
        Debug.Log($"GameState → {newState}");
    }

    private void OnEnter(GameState state)
    {
        switch (state)
        {
            case GameState.Boot:
                TransitionTo(GameState.MainMenu);
                break;
            case GameState.Playing:
                Time.timeScale = 1f;
                break;
            case GameState.Paused:
                Time.timeScale = 0f;
                break;
            case GameState.GameOver:
                EventBus<PlayerDiedEvent>.Publish(new PlayerDiedEvent());
                break;
            case GameState.GameCompleted:
                EventBus<GameCompletedEvent>.Publish(new GameCompletedEvent());
                break;
        }
    }

    private void OnExit(GameState state)
    {
        // cleanup per state if needed later
    }
}