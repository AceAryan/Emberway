using UnityEngine;

public abstract class Enemy : Entity
{
    [Header("Enemy Settings")]
    [SerializeField] protected float _moveSpeed = 3f;
    [SerializeField] protected int _damage = 1;
    [SerializeField] protected float _detectionRange = 5f;

    protected Transform _player;

    protected override void Awake()
    {
        base.Awake();
        _player = GameObject.FindGameObjectWithTag("Player")?.transform;
    }

    protected virtual void Update()
    {
        if (IsDead) return;
        UpdateBehavior();
    }

    // Each enemy type implements its own behavior
    protected abstract void UpdateBehavior();

    protected bool IsPlayerInRange()
    {
        if (_player == null) return false;
        return Vector2.Distance(transform.position, _player.position) <= _detectionRange;
    }

    public override void Die()
    {
        // enemies will have death animation/effects later
        Debug.Log($"{gameObject.name} defeated.");
        Destroy(gameObject);
    }

    private void OnDrawGizmosSelected()
    {
        Gizmos.color = Color.red;
        Gizmos.DrawWireSphere(transform.position, _detectionRange);
    }
}