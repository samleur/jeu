using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class TimeLoopManager : MonoBehaviour
{
    public GameObject playerPrefab;
    public Text timerText;
    public Button restartButton;
    public List<Vector3> recordedPositions = new List<Vector3>();
    private bool isRecording = true;
    private GameObject currentPlayer;
    public float loopDuration = 5f;
    private float timer;

    void Start()
    {
        restartButton.onClick.AddListener(RestartLoop);
        StartNewLoop();
    }

    void Update()
    {
        if (isRecording && currentPlayer != null)
        {
            recordedPositions.Add(currentPlayer.transform.position);
        }

        timer -= Time.deltaTime;
        timerText.text = "Time Left: " + timer.ToString("F2");
        
        if (timer <= 0)
        {
            RestartLoop();
        }
    }

    public void RestartLoop()
    {
        isRecording = false;
        SpawnGhost();
        StartNewLoop();
    }

    void StartNewLoop()
    {
        timer = loopDuration;
        currentPlayer = Instantiate(playerPrefab, Vector3.zero, Quaternion.identity);
        isRecording = true;
        recordedPositions.Clear();
    }

    void SpawnGhost()
    {
        GameObject ghost = Instantiate(playerPrefab, Vector3.zero, Quaternion.identity);
        ghost.GetComponent<PlayerController>().enabled = false;
        ghost.AddComponent<GhostReplay>().SetReplayData(recordedPositions);
    }
}

public class PlayerController : MonoBehaviour
{
    public float speed = 5f;
    private Rigidbody2D rb;

    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
    }
    
    void Update()
    {
        float moveX = Input.GetAxis("Horizontal") * speed;
        float moveY = Input.GetAxis("Vertical") * speed;
        rb.velocity = new Vector2(moveX, moveY);
    }
}

public class GhostReplay : MonoBehaviour
{
    private List<Vector3> replayPositions;
    private int index = 0;
    private float playbackSpeed = 0.1f;

    public void SetReplayData(List<Vector3> positions)
    {
        replayPositions = new List<Vector3>(positions);
        InvokeRepeating("ReplayMovement", 0f, playbackSpeed);
    }

    void ReplayMovement()
    {
        if (index < replayPositions.Count)
        {
            transform.position = replayPositions[index];
            index++;
        }
        else
        {
            CancelInvoke("ReplayMovement");
        }
    }
}
