export const redirectToCallingOnOngoingCall = async (router) => {
  try {
    const endpoint = 'https://bramka:443/api/call/ongoing';
    const response = await fetch(endpoint);
    const room = localStorage.getItem('room');
    if (response.status === 200) {
      const data = await response.json();

      if (data && data.call_status == "NOT_ANSWERED" && data.room == room) {
        router.push({ name: 'calling' });
      }
    }
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

export const handleUserActivation = async (router, provided_user) => {
    const endpoint = `https://bramka:443/api/enrollment/get?code=${provided_user}`;
    const requestOptions = {
      method: 'GET',
    };

    try {
      const response = await fetch(endpoint, requestOptions);
      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('user', provided_user);
        localStorage.setItem('room', data["room"]);

        const soundURL = new URL('/static/assets/activated.mp3', import.meta.url);
        const audio = new Audio(soundURL);
        audio.play();

        router.push({ name: 'standby' });
      } else {
        console.error('Error fetching data:', response.statusText);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    }
};

export const redirectToStandbyOnEndedCall = async (router, video) => {
 try {
    const endpoint = 'https://bramka:443/api/call/ongoing';
    const response = await fetch(endpoint);
    if (response.status === 202) {
        video._value.setAttribute("src", "../assets/standby.png")
        router.push({ name: 'standby' });
    }
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

export const markCallAsAnswered = async () => {
  try {
    const room = parseInt(localStorage.getItem('room'), 10);
    const endpoint = 'https://bramka:443/api/call';
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ room: room, call_status: "ANSWERED" }),
    };

    const response = await fetch(endpoint, requestOptions);
  } catch (error) {
    console.error('Error:', error);
  }
};

export const endCall = async () => {
  try {
    const room = parseInt(localStorage.getItem('room'), 10);
    const endpoint = 'https://bramka:443/api/call';
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ room: room, call_status: "INACTIVE" }),
    };

    const response = await fetch(endpoint, requestOptions);
  } catch (error) {
    console.error('Error:', error);
  }
};

export const openLock = async () => {
  try {
    const room = parseInt(localStorage.getItem('room'), 10);
    const endpoint = 'https://bramka:443/api/lock/control';
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ "operation": "OPEN" }),
    };

    const response = await fetch(endpoint, requestOptions);
  } catch (error) {
    console.error('Error:', error);
  }
};

export const getServerStatus = async () => {
  try {
    const endpoint = 'https://bramka:443/api/status/server';
    const requestOptions = {
      method: 'GET',
    };

    const response = await fetch(endpoint, requestOptions);

    if (response.status === 200) {
        return "ONLINE"
    }
    return "OFFLINE"

  } catch (error) {
    console.error('Error:', error);
  }
};

export const getDoorStatus = async () => {
  try {
    const endpoint = 'https://bramka:443/api/lock/policy/active';
    const requestOptions = {
      method: 'GET',
    };

    const response = await fetch(endpoint, requestOptions);
    const data = await response.json()

    if (data.policies.length === 0) {
        return "CLOSED"
    }

    return "OPEN"

  } catch (error) {
    console.error('Error:', error);
  }
};

export const fetchPoliciesData = async () => {
  try {
    const response = await fetch('https://bramka:443/api/lock/policy');
    if (response.ok) {
      const data = await response.json();

      let order = {
        "MONDAY": 1,
        "TUESDAY": 2,
        "WEDNESDAY": 3,
        "THURSDAY": 4,
        "FRIDAY": 5,
        "SATURDAY": 6,
        "SUNDAY": 7
      }

      let policies = data.policies.map((policy) => ({
        id: policy.id,
        order: order[policy.day],
        day: policy.day,
        start: policy.start_time.slice(0, 8),
        end: policy.end_time.slice(0, 8),
        active: policy.active === 'True' ? 'Active' : 'Inactive',
      }));

      policies.sort((a, b) => {
        if(a.order < b.order) return -1;
        if(a.order > b.order) return 1;
        return 0;
      })

      return policies;
    } else {
      console.error('Failed to fetch data');
    }
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};