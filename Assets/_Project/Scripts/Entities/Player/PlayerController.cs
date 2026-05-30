using UnityEngine;
using UnityEngine.InputSystem;

public class PlayerController : Entity  
{
    [Header("Movement")]
    [SerializeField] private float _moveSpeed = 8f;
    [SerializeField] private float _jumpForce = 16f;
    [SerializeField] private Transform _groundCheck;
    [SerializeField] private LayerMask _groundLayer;

    private Rigidbody2D _rb;
    private Vector2 _moveInput;
    private bool _isGrounded;
    private Animator _animator;
    public bool IsGrounded => _isGrounded;
    public bool IsMoving => Mathf.Abs(_moveInput.x) > 0.1f;
    public bool IsFalling => _rb.linearVelocity.y < -0.1f;
    public bool IsJumping => _rb.linearVelocity.y > 0.1f;

    protected override void Awake()
    {
        base.Awake(); // Call Entity's Awake to initialize HealthComponent
        _rb = GetComponent<Rigidbody2D>();
        _animator = GetComponent<Animator>();
    }

    private void Update()
    {
        CheckGround();
    }

    // Using FixedUpdate for physics-based movement to ensure consistent behavior regardless of frame rate
    private void FixedUpdate()
    {
        Move();
    }

    // Called automatically by Unity's Input System
    public void OnMove(InputValue value)
    {
        _moveInput = value.Get<Vector2>();
    }

    public void OnJump(InputValue value)
    {
        if (value.isPressed && _isGrounded)
        {
            _rb.linearVelocity = new Vector2(_rb.linearVelocity.x, _jumpForce);
        }
    }

    private void Move()
    {
        _rb.linearVelocity = new Vector2(_moveInput.x * _moveSpeed, _rb.linearVelocity.y);
        _animator.SetFloat("Speed", Mathf.Abs(_moveInput.x));

        // Flip the player's sprite based on movement direction
        if (_moveInput.x > 0)
            transform.localScale = new Vector3(1, 1, 1);
        else if (_moveInput.x < 0)
            transform.localScale = new Vector3(-1, 1, 1);
    }

    // Checks if the player is currently touching the ground using a small circle overlap for jump logic
    private void CheckGround()
    {
        _isGrounded = Physics2D.OverlapCircle(_groundCheck.position, 0.1f, _groundLayer);
    }

    // debugging aid to visualize the ground check area in the editor
    private void OnDrawGizmosSelected()
    {
        if (_groundCheck != null)
        {
            Gizmos.color = Color.green;
            Gizmos.DrawWireSphere(_groundCheck.position, 0.1f);
        }
    }
}