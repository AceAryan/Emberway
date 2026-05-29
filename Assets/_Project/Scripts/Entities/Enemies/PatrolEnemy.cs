using UnityEngine;

public class PatrolEnemy : Enemy
{
    [Header("Patrol Settings")]
    [SerializeField] private float _patrolDistance = 4f;

    private Vector2 _startPosition;
    private int _direction = 1;

    protected override void Awake()
    {
        base.Awake();
        _startPosition = transform.position;
    }

    protected override void UpdateBehavior()
    {
        if (IsPlayerInRange())
            ChasePlayer();
        else
            Patrol();
    }

    private void Patrol()
    {
        transform.Translate(Vector2.right * _direction * _moveSpeed * Time.deltaTime);

        float distanceFromStart = transform.position.x - _startPosition.x;
        if (Mathf.Abs(distanceFromStart) >= _patrolDistance)
            _direction *= -1; // flip direction
    }

    private void ChasePlayer()
    {
        Vector2 directionToPlayer = (_player.position - transform.position).normalized;
        transform.Translate(directionToPlayer * _moveSpeed * Time.deltaTime);
    }
}