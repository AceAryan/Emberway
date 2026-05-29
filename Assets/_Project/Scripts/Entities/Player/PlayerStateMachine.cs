using UnityEngine;

public enum PlayerState
{
    Idle,
    Running,
    Jumping,
    Falling,
    Hurt,
    Dead
}

// PlayerStateMachine is responsible for managing the player's current state based on input and physics conditions,
// separating state logic from the PlayerController which handles input and movement. 
public class PlayerStateMachine : MonoBehaviour
{
    private PlayerState _currentState;
    public PlayerState CurrentState => _currentState;

    private PlayerController _controller;

    private void Awake()
    {
        _controller = GetComponent<PlayerController>();
        TransitionTo(PlayerState.Idle);
    }

    private void Update()
    {
        UpdateState();
    }

    private void UpdateState()
    {
        switch (_currentState)
        {
            case PlayerState.Idle:
                if (_controller.IsMoving)
                    TransitionTo(PlayerState.Running);
                if (_controller.IsFalling)
                    TransitionTo(PlayerState.Falling);
                break;

            case PlayerState.Running:
                if (!_controller.IsMoving)
                    TransitionTo(PlayerState.Idle);
                if (_controller.IsFalling)
                    TransitionTo(PlayerState.Falling);
                break;

            case PlayerState.Jumping:
                if (_controller.IsFalling)
                    TransitionTo(PlayerState.Falling);
                break;

            case PlayerState.Falling:
                if (_controller.IsGrounded)
                    TransitionTo(_controller.IsMoving ? PlayerState.Running : PlayerState.Idle);
                break;

            case PlayerState.Hurt:
                // will handle later when we add health
                break;

            case PlayerState.Dead:
                // nothing allowed in dead state
                break;
        }
    }

    public void TransitionTo(PlayerState newState)
    {
        if (_currentState == newState) return;

        OnExit(_currentState);
        _currentState = newState;
        OnEnter(newState);

        Debug.Log($"PlayerState → {newState}");
    }

    private void OnEnter(PlayerState state)
    {
        switch (state)
        {
            case PlayerState.Dead:
                EventBus<PlayerDiedEvent>.Publish(new PlayerDiedEvent());
                break;
        }
    }

    private void OnExit(PlayerState state)
    {
        // cleanup per state if needed
    }
}