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

    private void OnEnable()
    {
        EventBus<PlayerDiedEvent>.Subscribe(HandlePlayerDied);
    }

    private void OnDisable()
    {
        EventBus<PlayerDiedEvent>.Unsubscribe(HandlePlayerDied);
    }

    private void Start()
    {
        // Enter Boot directly (TransitionTo would skip it, since Boot is already the default value),
        // finish booting, THEN move on. Transitions never happen from inside OnEnter.
        _currentState = GameState.Boot;
        OnEnter(GameState.Boot);
        Debug.Log($"GameState → {GameState.Boot}");

        TransitionTo(GameState.MainMenu);
    }

    public void TransitionTo(GameState newState)
    {
        if (_currentState == newState) return;

        OnExit(_currentState);
        _currentState = newState;
        Debug.Log($"GameState → {newState}");
        OnEnter(newState);
    }

    // GameManager LISTENS for player death; it does not announce it.
    private void HandlePlayerDied(PlayerDiedEvent evt)
    {
        TransitionTo(GameState.GameOver);
    }

    private void OnEnter(GameState state)
    {
        switch (state)
        {
            case GameState.Boot:
                // load settings / save data here later
                break;
            case GameState.Playing:
                Time.timeScale = 1f;
                break;
            case GameState.Paused:
                Time.timeScale = 0f;
                break;
            case GameState.GameOver:
                // show game over UI / respawn flow later (Phase 5)
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
