import {
  Alert,
  Badge,
  Button,
  Card,
  Container,
  Group,
  MantineProvider,
  PasswordInput,
  Popover,
  Stack,
  Tabs,
  Text,
  Textarea,
  TextInput,
  Title,
} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { useEffect, useState } from "react";

type User = {
    id: number;
    username: string;
    displayName: string;
    bio: string;
    plan: string;
};

type Post = {
    id: number;
    content: string;
    createdAt: string;
    userId: number;
    displayName: string;
    username: string;
    plan: string;
};

function VerifiedBadge({
    isOwn,
    currentUserPlan,
}: {
    isOwn: boolean;
    currentUserPlan: string;
}) {
    const [opened, { close, toggle }] = useDisclosure(false);

    return (
        <Popover opened={opened} onClose={close} withArrow>
            <Popover.Target>
                <Badge
                    color="blue"
                    ml="xs"
                    size="sm"
                    style={{ cursor: "pointer" }}
                    onClick={toggle}
                >
                    ✓
                </Badge>
            </Popover.Target>
            <Popover.Dropdown>
                <Text size="sm">
                    {isOwn
                        ? "You are verified."
                        : "This user is verified."}
                </Text>
                {!isOwn && currentUserPlan !== "premium" && (
                    <Text size="xs" c="dimmed" mt="xs">
                        Subscribe to Z Premium to get verified!
                    </Text>
                )}
            </Popover.Dropdown>
        </Popover>
    );
}

function Auth({ onAuth }: { onAuth: (u: User) => void }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [isRegister, setIsRegister] = useState(false);

    const submit = async () => {
        const endpoint = isRegister ? "/api/register" : "/api/login";
        const res = await fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }),
        });
        const data = await res.json();
        if (res.ok) {
            onAuth(data);
        } else {
            setError(data.error);
        }
    };

    return (
        <Container size="xs" py="xl">
            <Title order={1} ta="center" mb="lg">
                Z
            </Title>
            <Stack>
                <TextInput
                    label="Username"
                    value={username}
                    onChange={(e) => setUsername(e.currentTarget.value)}
                />
                <PasswordInput
                    label="Password"
                    value={password}
                    onChange={(e) => setPassword(e.currentTarget.value)}
                />
                {error && <Alert color="red">{error}</Alert>}
                <Button onClick={submit}>
                    {isRegister ? "Register" : "Login"}
                </Button>
                <Button
                    variant="subtle"
                    onClick={() => setIsRegister(!isRegister)}
                >
                    {isRegister
                        ? "Already have an account? Login"
                        : "Don't have an account? Register"}
                </Button>
            </Stack>
        </Container>
    );
}

function Timeline({ user }: { user: User }) {
    const [postList, setPostList] = useState<Post[]>([]);
    const [content, setContent] = useState("");

    const fetchPosts = () => {
        fetch("/api/posts")
            .then((r) => r.json())
            .then(setPostList);
    };

    useEffect(() => {
        fetchPosts();
    }, []);

    const submit = async () => {
        if (!content.trim()) return;
        await fetch("/api/posts", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ content }),
        });
        setContent("");
        fetchPosts();
    };

    return (
        <Stack>
            <Group align="end">
                <Textarea
                    style={{ flex: 1 }}
                    placeholder="What's happening?"
                    value={content}
                    onChange={(e) => setContent(e.currentTarget.value)}
                />
                <Button onClick={submit}>Post</Button>
            </Group>
            {postList.map((post) => (
                <Card key={post.id} withBorder>
                    <Group mb="xs">
                        <Text fw={700}>
                            {post.displayName}
                            {post.plan === "premium" && (
                                <VerifiedBadge
                                    isOwn={post.userId === user.id}
                                    currentUserPlan={user.plan}
                                />
                            )}
                        </Text>
                        <Text size="sm" c="dimmed">
                            @{post.username}
                        </Text>
                    </Group>
                    <Text>{post.content}</Text>
                    <Text size="xs" c="dimmed" mt="xs">
                        {new Date(post.createdAt).toLocaleString()}
                    </Text>
                </Card>
            ))}
        </Stack>
    );
}

function Profile({
    user,
    setUser,
}: {
    user: User;
    setUser: (u: User) => void;
}) {
    const [displayName, setDisplayName] = useState(user.displayName);
    const [bio, setBio] = useState(user.bio);
    const [message, setMessage] = useState("");

    const save = async () => {
        const res = await fetch("/api/me", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ displayName, bio }),
        });
        if (res.ok) {
            const updated = await res.json();
            setUser(updated);
            setMessage("Profile updated!");
        }
    };

    return (
        <Stack>
            <TextInput
                label="Display Name"
                value={displayName}
                onChange={(e) => setDisplayName(e.currentTarget.value)}
            />
            <Textarea
                label="Bio"
                value={bio}
                onChange={(e) => setBio(e.currentTarget.value)}
            />
            <Button onClick={save}>Save</Button>
            {message && <Alert color="green">{message}</Alert>}
        </Stack>
    );
}

function Premium({ user }: { user: User }) {
    const [error, setError] = useState("");
    const [flag, setFlag] = useState<string | null>(null);

    useEffect(() => {
        if (user.plan === "premium") {
            fetch("/api/flag")
                .then((r) => r.json())
                .then((data) => setFlag(data.flag));
        }
    }, [user.plan]);

    const upgrade = async () => {
        setError("");
        const res = await fetch("/api/upgrade", { method: "POST" });
        if (!res.ok) {
            const data = await res.json();
            setError(data.error);
        }
    };

    if (user.plan === "premium") {
        return (
            <Stack>
                <Alert color="green">You are a Z Premium subscriber!</Alert>
                {flag && (
                    <Alert color="yellow" title="Premium Content">
                        {flag}
                    </Alert>
                )}
            </Stack>
        );
    }

    return (
        <Stack>
            <Title order={3}>Z Premium</Title>
            <Text>Get a verified badge next to your name!</Text>
            <Card withBorder>
                <Title order={4}>Z Premium</Title>
                <Text size="xl" fw={700}>
                    ¥5,000,000,000,000,000 / month
                </Text>
                <Button mt="md" onClick={upgrade}>
                    Subscribe
                </Button>
            </Card>
            {error && <Alert color="red">{error}</Alert>}
        </Stack>
    );
}

function Main({
    user,
    setUser,
}: {
    user: User;
    setUser: (u: User | null) => void;
}) {
    const [tab, setTab] = useState<string | null>("timeline");

    const logout = async () => {
        await fetch("/api/logout", { method: "POST" });
        setUser(null);
    };

    return (
        <Container size="sm" py="md">
            <Group justify="space-between" mb="md">
                <Title order={2}>Z</Title>
                <Group>
                    <Text>
                        {user.displayName}
                        {user.plan === "premium" && (
                            <VerifiedBadge
                                isOwn={true}
                                currentUserPlan={user.plan}
                            />
                        )}
                    </Text>
                    <Button variant="subtle" size="xs" onClick={logout}>
                        Logout
                    </Button>
                </Group>
            </Group>
            <Tabs value={tab} onChange={setTab}>
                <Tabs.List>
                    <Tabs.Tab value="timeline">Timeline</Tabs.Tab>
                    <Tabs.Tab value="profile">Profile</Tabs.Tab>
                    <Tabs.Tab value="premium">Z Premium</Tabs.Tab>
                </Tabs.List>
                <Tabs.Panel value="timeline" pt="md">
                    <Timeline user={user} />
                </Tabs.Panel>
                <Tabs.Panel value="profile" pt="md">
                    <Profile user={user} setUser={(u) => setUser(u)} />
                </Tabs.Panel>
                <Tabs.Panel value="premium" pt="md">
                    <Premium user={user} />
                </Tabs.Panel>
            </Tabs>
        </Container>
    );
}

export default function App() {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch("/api/me")
            .then((r) => (r.ok ? r.json() : null))
            .then((u) => {
                setUser(u);
                setLoading(false);
            });
    }, []);

    if (loading) return null;

    return (
        <MantineProvider>
            {user
                ? <Main user={user} setUser={setUser} />
                : <Auth onAuth={setUser} />}
        </MantineProvider>
    );
}
