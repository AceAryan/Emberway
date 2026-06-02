using UnityEngine;

public class AttackHitbox : MonoBehaviour
{
    [SerializeField] private int _damage = 1;

    private void OnTriggerEnter2D(Collider2D other)
    {
        if (other.CompareTag("Enemy"))
        {
            Entity entity = other.GetComponent<Entity>();
            entity?.TakeDamage(_damage);
            Debug.Log($"Hit {other.name} for {_damage} damage");
        }
    }
}