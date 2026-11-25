using UnityEngine;

// abstract base class for all entities in the game (player, enemies, destructible objects) that can take damage and die.
// abstract because we don't want to create generic entities, only specific types like Player or Enemy that inherit from this base class.
public abstract class Entity : MonoBehaviour
{
    protected HealthComponent _health;

    // virtual so that derived classes can override it if they need to do additional setup in Awake (e.g. initialize other components)
    protected virtual void Awake()
    {
        _health = GetComponent<HealthComponent>();

        // When health hits 0, run this entity's Die().
        // Die is virtual, so the override (Enemy.Die, PlayerController.Die) is what actually runs.
        if (_health != null)
            _health.Died += Die;
    }

    // Always unsubscribe from events you subscribed to, so no dangling references remain.
    protected virtual void OnDestroy()
    {
        if (_health != null)
            _health.Died -= Die;
    }

    public virtual void TakeDamage(int amount)
    {
        _health?.TakeDamage(amount);
    }

    public virtual void Die()
    {
        Destroy(gameObject);
    }

    public bool IsDead => _health != null && _health.IsDead;
}
