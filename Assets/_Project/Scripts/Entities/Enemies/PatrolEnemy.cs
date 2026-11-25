using UnityEngine;

public class PatrolEnemy : Enemy
{
    [Header("Patrol Settings")]
    [SerializeField] private float _patrolDistance = 4f;

    private Vector2 _startPosition;
    private int _direction = 1;
    private Rigidbody2D _rb;

    protected override void Awake()
    {
        base.Awake();
        _startPosition = transform.position;
        _rb = GetComponent<Rigidbody2D>();
    }

    protected override void UpdateBehavior()
    {
        if (IsPlayerInRange())
            ChasePlayer();
        else
            Patrol();
    }

    // TODO (you): Phase 0 Task 2 - enemy jitters in place after chasing; also move velocity writes to FixedUpdate.
    private void Patrol()
    {
        float distanceFromStart = transform.position.x - _startPosition.x;
        if (Mathf.Abs(distanceFromStart) >= _patrolDistance)
            _direction *= -1; // flip direction
        _rb.linearVelocity = new Vector2(_direction * _moveSpeed, _rb.linearVelocity.y);
    }

    private void ChasePlayer()
    {
        float dirx = _player.position.x > transform.position.x ? 1 : -1;
        _rb.linearVelocity = new Vector2(dirx * _moveSpeed, _rb.linearVelocity.y);
    }
}