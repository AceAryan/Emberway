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